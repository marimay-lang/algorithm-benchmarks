"""Durable observations and integrity checkpoints for a catalogue run."""

from __future__ import annotations

import json
import os
from pathlib import Path
import statistics
import sys
import tempfile

from catalog_contract import require, source_hashes
from perf_protocol import sha256_file


def verify_inputs(repository, sources, binaries, anchors):
    current = source_hashes(repository)
    changed = [
        path for path in sorted(sources.keys() | current.keys())
        if sources.get(path) != current.get(path)
    ]
    for path, digest in (binaries | anchors).items():
        actual = Path(path)
        if not actual.is_absolute():
            actual = repository / actual
        if not actual.is_file() or sha256_file(actual) != digest:
            changed.append(path)
    require(
        not changed,
        "benchmark inputs changed; measurements are diagnostic only: "
        + ", ".join(changed),
    )


def diagnostic_table(header, events, reason):
    meta = header["metadata"]
    participants = meta["participants"]
    values = {w: {p: [] for p in participants} for w in header["workloads"]}
    failed = set()
    for event in events:
        key = event["workload"], event["participant"]
        if event["status"] == "failed":
            failed.add(key)
        elif event["status"] == "passed" and event["phase"] == "sample":
            values[key[0]][key[1]].append(event["elapsed_ms"])
    lines = ["Saved observations — diagnostic only", str(reason)]
    for workload, engines in values.items():
        cells = []
        for participant, samples in engines.items():
            if (workload, participant) in failed:
                value = "FAILED"
            else:
                value = f"{statistics.median(samples):.2f} ms" if samples else "—"
            cells.append(f"{participant}={value} [{len(samples)}/{meta['samples']}]")
        lines.append(f"{workload}: " + ", ".join(cells))
    return "\n".join(lines)


def show_journal(path):
    records = []
    # A process killed during the last write may leave one incomplete tail.
    with Path(path).open(encoding="utf-8") as source:
        for line in source:
            if not line.endswith("\n"):
                break
            records.append(json.loads(line))
    require(bool(records), "empty observation journal")
    header = records[0]
    require(header.get("schema") == "marimay.catalog-run-journal/1", "unknown journal")
    events = [r["event"] for r in records[1:] if r.get("kind") == "observation"]
    ending = records[-1]
    reason = ending.get("error", "Incomplete run; final integrity was not verified")
    if ending.get("kind") == "complete":
        reason = f"Recorded run status: {ending['status']}"
    return diagnostic_table(header, events, reason)


class RunJournal:
    def __init__(self, directory, metadata, workloads, commands):
        directory.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix="run-", suffix=".jsonl", dir=directory)
        self.path = Path(name)
        self.file = os.fdopen(descriptor, "w", encoding="utf-8")
        self.header = {
            "schema": "marimay.catalog-run-journal/1",
            "kind": "start",
            "metadata": metadata,
            "workloads": workloads,
            "commands": commands,
        }
        self.events = []

    def write(self, record):
        self.file.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
        self.file.flush()

    def __enter__(self):
        try:
            self.write(self.header)
        except BaseException:
            self.file.close()
            raise
        print(f"Observation journal: {self.path}", flush=True)
        return self

    def observe(self, event):
        self.write({"kind": "observation", "event": event})
        self.events.append(dict(event))

    def complete(self, status):
        self.write({"kind": "complete", "status": status})

    def __exit__(self, kind, error, traceback):
        try:
            if error is not None:
                reason = str(error) or kind.__name__
                try:
                    self.write({"kind": "aborted", "error": reason})
                except OSError:
                    pass  # Preserve the original failure and earlier flushed rows.
                print(diagnostic_table(self.header, self.events, reason), flush=True)
                print(f"Saved observations: {self.path}", file=sys.stderr, flush=True)
        finally:
            self.file.close()
