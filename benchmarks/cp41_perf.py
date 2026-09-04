#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import pathlib
import platform
import statistics
import subprocess
import sys
from typing import Any

from perf_environment import cpu_name, git_revision
from perf_protocol import ProtocolError, schedule, validate_run_shape, load_protocol


SCHEMA = "marimay.cp41-hardware-counters/2"
WORKLOADS = ("stack", "queue", "heap-sort", "min-heap")
EVENTS = (
    "cycles",
    "instructions",
    "branches",
    "branch-misses",
    "cache-references",
    "cache-misses",
)
DEFAULT_EVENT_PROFILE = "perf-generic-v1"
EVENT_PROFILES = {
    DEFAULT_EVENT_PROFILE: {event: event for event in EVENTS},
    "linux-l1d-loads-v1": {
        "cycles": "cycles",
        "instructions": "instructions",
        "branches": "branches",
        "branch-misses": "branch-misses",
        "cache-references": "L1-dcache-loads",
        "cache-misses": "L1-dcache-load-misses",
    },
}
CHECKSUMS = {
    "stack": 498055372,
    "queue": 498106199,
    "heap-sort": 999995320,
    "min-heap": 405398755,
}


def event_profile(name: str) -> dict[str, str]:
    try:
        profile = EVENT_PROFILES[name]
    except KeyError as error:
        raise ProtocolError(f"unsupported hardware-counter profile: {name}") from error
    if set(profile) != set(EVENTS) or len(set(profile.values())) != len(EVENTS):
        raise ProtocolError(f"invalid hardware-counter profile: {name}")
    return profile


def parse_perf_csv(
    text: str, profile_name: str = DEFAULT_EVENT_PROFILE
) -> dict[str, int]:
    profile = event_profile(profile_name)
    logical_by_physical = {
        physical: logical for logical, physical in profile.items()
    }
    counters: dict[str, int] = {}
    for row in csv.reader(io.StringIO(text)):
        if len(row) < 3:
            continue
        physical_event = row[2].strip().split(":", 1)[0]
        if physical_event not in logical_by_physical:
            continue
        event = logical_by_physical[physical_event]
        value = row[0].strip()
        try:
            parsed = float(value)
        except ValueError as error:
            raise ProtocolError(
                f"hardware counter {event} is unavailable: {value or '<empty>'}"
            ) from error
        if not parsed.is_integer() or parsed <= 0:
            raise ProtocolError(f"invalid hardware counter {event}: {value}")
        counters[event] = int(parsed)
    missing = [event for event in EVENTS if event not in counters]
    if missing:
        raise ProtocolError(
            "perf did not report required counters: " + ", ".join(missing)
        )
    return counters


def summarize(values: list[int]) -> dict[str, float]:
    if not values or any(value <= 0 for value in values):
        raise ProtocolError("counter samples must be positive")
    ordered = sorted(float(value) for value in values)
    median = float(statistics.median(ordered))
    midpoint = len(ordered) // 2
    lower = ordered[:midpoint]
    upper = ordered[midpoint + (len(ordered) % 2) :]
    q1 = float(statistics.median(lower))
    q3 = float(statistics.median(upper))
    mad = float(statistics.median(abs(value - median) for value in ordered))
    return {
        "median": median,
        "mad": mad,
        "min": ordered[0],
        "max": ordered[-1],
        "noise_fraction": max(0.02, 3.0 * mad / median, (q3 - q1) / median),
    }


def run_observation(
    perf: pathlib.Path,
    binary: pathlib.Path,
    workload: str,
    cpu: int,
    event_profile_name: str,
) -> tuple[dict[str, int], list[str]]:
    profile = event_profile(event_profile_name)
    command = [
        str(perf),
        "stat",
        "--no-big-num",
        "-x,",
        "-e",
        ",".join(profile[event] for event in EVENTS),
        "--",
        "taskset",
        "-c",
        str(cpu),
        str(binary),
    ]
    completed = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=300,
    )
    expected = f"{workload} {CHECKSUMS[workload]}\n"
    if completed.returncode != 0:
        raise ProtocolError(
            f"perf observation failed with exit {completed.returncode}: "
            f"{completed.stderr.strip()}"
        )
    if completed.stdout != expected:
        raise ProtocolError(
            f"checksum observation mismatch for {workload}: "
            f"stdout={completed.stdout!r}, expected={expected!r}"
        )
    return parse_perf_csv(completed.stderr, event_profile_name), command


def preflight(
    perf: pathlib.Path, event_profile_name: str
) -> tuple[dict[str, int], list[str]]:
    allowed = sorted(os.sched_getaffinity(0))
    if not allowed:
        raise ProtocolError("runner exposes no eligible CPU for taskset")
    profile = event_profile(event_profile_name)
    command = [
        str(perf),
        "stat",
        "--no-big-num",
        "-x,",
        "-e",
        ",".join(profile[event] for event in EVENTS),
        "--",
        "taskset",
        "-c",
        str(allowed[0]),
        sys.executable,
        "-c",
        "a=bytearray(64 * 1024 * 1024); print(sum(a[::64]))",
    ]
    completed = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )
    if completed.returncode != 0:
        raise ProtocolError(
            f"hardware-counter preflight failed with exit {completed.returncode}: "
            f"{completed.stderr.strip()}"
        )
    if completed.stdout != "0\n":
        raise ProtocolError(
            f"hardware-counter preflight workload drifted: {completed.stdout!r}"
        )
    return parse_perf_csv(completed.stderr, event_profile_name), command


def collect(
    repository: pathlib.Path,
    binary_dir: pathlib.Path,
    perf: pathlib.Path,
    phase: str,
    compiler_revision: str,
    warmups: int,
    samples: int,
    event_profile_name: str = DEFAULT_EVENT_PROFILE,
) -> dict[str, Any]:
    _, protocol = load_protocol(repository)
    validate_run_shape(protocol, warmups, samples)
    binaries = {
        workload: binary_dir / f"marimay-{workload}" for workload in WORKLOADS
    }
    for binary in binaries.values():
        if not binary.is_file() or not os.access(binary, os.X_OK):
            raise ProtocolError(f"benchmark binary is not executable: {binary}")
    allowed = sorted(os.sched_getaffinity(0))
    if not allowed:
        raise ProtocolError("runner exposes no eligible CPU for taskset")
    cpu = allowed[0]
    raw = {
        workload: {event: [] for event in EVENTS} for workload in WORKLOADS
    }
    observations: list[dict[str, Any]] = []
    command_template: list[str] = []
    load_start = list(os.getloadavg())
    for event in schedule(WORKLOADS, ("marimay",), warmups, samples):
        workload = str(event["workload"])
        counters, command_template = run_observation(
            perf, binaries[workload], workload, cpu, event_profile_name
        )
        observation = {
            "phase": event["phase"],
            "round": event["round"],
            "workload": workload,
            "counters": counters,
        }
        observations.append(observation)
        if event["phase"] == "sample":
            for counter, value in counters.items():
                raw[workload][counter].append(value)
    return {
        "schema": SCHEMA,
        "phase": phase,
        "compiler_revision": compiler_revision,
        "corpus_revision": git_revision(repository, repository),
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "cpu": cpu_name(),
            "logical_cpus": os.cpu_count() or 1,
            "pinned_cpu": cpu,
        },
        "isolation": {
            "mode": "dedicated-runner-contract",
            "load_average_at_start": load_start,
            "load_average_at_end": list(os.getloadavg()),
            "sample_selection": "none",
        },
        "protocol": {"warmups": warmups, "samples": samples, "order": "rotating-balanced-v1"},
        "perf": {
            "path": str(perf),
            "version": subprocess.run(
                [str(perf), "--version"], check=True, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30
            ).stdout.strip(),
            "logical_events": list(EVENTS),
            "event_profile": event_profile_name,
            "event_map": event_profile(event_profile_name),
            "command_shape": command_template,
        },
        "raw": raw,
        "summary": {
            workload: {
                event: summarize(raw[workload][event]) for event in EVENTS
            }
            for workload in WORKLOADS
        },
        "observations": observations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect balanced CP41 Linux hardware-counter observations."
    )
    parser.add_argument("--binary-dir", type=pathlib.Path)
    parser.add_argument("--perf", type=pathlib.Path, required=True)
    parser.add_argument("--phase", choices=("before", "after"))
    parser.add_argument("--compiler-revision")
    parser.add_argument("--warmups", type=int, default=3)
    parser.add_argument("--samples", type=int, default=11)
    parser.add_argument(
        "--event-profile",
        choices=tuple(EVENT_PROFILES),
        default=DEFAULT_EVENT_PROFILE,
    )
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()
    repository = pathlib.Path(__file__).resolve().parents[1]
    try:
        if args.preflight:
            counters, _ = preflight(args.perf.resolve(), args.event_profile)
            print(
                "hardware-counter preflight ok: "
                + ", ".join(f"{event}={counters[event]}" for event in EVENTS)
            )
            return 0
        missing = [
            option
            for option, value in (
                ("--binary-dir", args.binary_dir),
                ("--phase", args.phase),
                ("--compiler-revision", args.compiler_revision),
                ("--output", args.output),
            )
            if value is None
        ]
        if missing:
            parser.error("collection requires " + ", ".join(missing))
        assert args.binary_dir is not None
        assert args.phase is not None
        assert args.compiler_revision is not None
        assert args.output is not None
        report = collect(
            repository, args.binary_dir.resolve(), args.perf.resolve(),
            args.phase, args.compiler_revision, args.warmups, args.samples,
            args.event_profile,
        )
    except (OSError, subprocess.SubprocessError, ProtocolError) as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
