from __future__ import annotations

import datetime as dt
import os
import pathlib
import platform
import re
import shutil
import shlex
import subprocess
import sys
from collections.abc import Sequence
from typing import Any

from perf_protocol import ProtocolError, sha256_file, tier1_target


def run_checked(
    command: Sequence[str],
    *,
    cwd: pathlib.Path,
    timeout: int = 300,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def tool_version(
    command: Sequence[str],
    cwd: pathlib.Path,
    *,
    accept_nonzero_output: bool = False,
) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=not accept_nonzero_output,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return "unavailable"
    output = completed.stdout.strip() or completed.stderr.strip()
    return output.splitlines()[0] if output else "unknown"


def git_revision(path: pathlib.Path, cwd: pathlib.Path) -> str:
    return tool_version(["git", "-C", str(path), "rev-parse", "HEAD"], cwd)


def cpu_name() -> str:
    if sys.platform == "darwin":
        try:
            return subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            ).strip()
        except (OSError, subprocess.SubprocessError):
            pass
    if sys.platform.startswith("linux"):
        try:
            for line in pathlib.Path("/proc/cpuinfo").read_text(
                encoding="utf-8"
            ).splitlines():
                if line.startswith(("model name", "Hardware")):
                    return line.split(":", 1)[1].strip()
        except (OSError, UnicodeError, IndexError):
            pass
    return platform.processor() or platform.machine()


def platform_id() -> str:
    target = tier1_target(platform.system(), platform.machine())
    cpu = re.sub(r"[^a-z0-9]+", "-", cpu_name().lower()).strip("-")
    if target.startswith("macos-") and cpu.startswith("apple-"):
        return f"{target}-{cpu}"
    return target


def native_tool_version(
    compiler: pathlib.Path,
    repository: pathlib.Path,
    config: dict[str, str],
    system: str,
) -> str:
    windows = system.lower() == "windows"
    live = tool_version(
        [str(compiler), "/Bv" if windows else "--version"],
        repository,
        accept_nonzero_output=windows,
    )
    configured_id = config.get("RUDA_NATIVE_C_COMPILER_ID", "")
    configured_version = config.get("RUDA_NATIVE_C_COMPILER_VERSION", "")
    configured = " ".join(
        value for value in (configured_id, configured_version) if value
    )
    if live in {"unavailable", "unknown"}:
        return configured or live
    if configured and configured.lower() not in live.lower():
        return f"{live}; configured {configured}"
    return live


def _version_lines(ruda_binary: pathlib.Path, repository: pathlib.Path) -> list[str]:
    try:
        completed = run_checked([str(ruda_binary), "--version"], cwd=repository)
    except (OSError, subprocess.SubprocessError) as error:
        raise ProtocolError(f"cannot execute Ruda compiler: {error}") from error
    return completed.stdout.splitlines()


def _runtime_version(version_lines: Sequence[str]) -> str:
    for line in version_lines:
        if line.startswith("runtime "):
            return line.split(" ", 1)[1]
    raise ProtocolError("Ruda --version does not report a runtime version")


def _manifest(path: pathlib.Path) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise ProtocolError(f"cannot read runtime manifest {path}: {error}") from error
    if not lines or lines[0] != "ruda-native-runtime-v1":
        raise ProtocolError(f"unsupported runtime manifest: {path}")
    result: dict[str, str] = {}
    for line in lines[1:]:
        if "=" not in line:
            raise ProtocolError(f"malformed runtime manifest line: {line!r}")
        key, value = line.split("=", 1)
        if not key or not value or key in result:
            raise ProtocolError(f"malformed runtime manifest field: {line!r}")
        result[key] = value
    required = {"profile", "runtime", "host", "processor", "compiler"}
    if set(result) != required:
        raise ProtocolError("runtime manifest metadata is incomplete")
    return result


def locate_runtime(
    ruda_binary: pathlib.Path, version_lines: Sequence[str]
) -> tuple[pathlib.Path, pathlib.Path, dict[str, str]]:
    release_directory = pathlib.Path("native-runtime") / "release"
    runtime_version = _runtime_version(version_lines)
    candidates = [
        ruda_binary.parent / release_directory,
        ruda_binary.parent.parent
        / "lib"
        / "ruda"
        / runtime_version
        / "native"
        / "release",
    ]
    archive_names = [
        "libruda_native_runtime_release.a",
        "ruda_native_runtime_release.lib",
    ]
    for directory in candidates:
        manifest_path = directory / "ruda-native-runtime.manifest"
        archive_path = next(
            (directory / name for name in archive_names if (directory / name).is_file()),
            None,
        )
        if manifest_path.is_file() and archive_path is not None:
            values = _manifest(manifest_path)
            if values["profile"] != "release":
                raise ProtocolError(
                    f"wrong runtime profile in {manifest_path}: {values['profile']}"
                )
            return manifest_path, archive_path, values
    raise ProtocolError(
        "cannot locate the release runtime manifest/archive beside the Ruda compiler"
    )


def _build_config(ruda_binary: pathlib.Path) -> dict[str, str]:
    path = ruda_binary.parent / "generated" / "ruda" / "build_config.h"
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    pattern = re.compile(r'^#define (RUDA_NATIVE_C_[A-Z_]+) "(.*)"$')
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            match = pattern.match(line)
            if match:
                values[match.group(1)] = match.group(2)
    except (OSError, UnicodeError) as error:
        raise ProtocolError(f"cannot read {path}: {error}") from error
    return values


def _native_flags(config: dict[str, str]) -> list[str]:
    sanitizer = config.get("RUDA_NATIVE_C_SANITIZER_FLAG", "")
    if os.name == "nt":
        flags = ["/nologo", "/std:c17", "/W4", "/WX", "/fp:strict", "/O2"]
    else:
        flags = [
            "-std=c17",
            "-O2",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Wconversion",
            "-Wshadow",
            "-Werror",
            "-fno-fast-math",
            "-frounding-math",
            "-ffp-contract=off",
            "-fexcess-precision=standard",
            "-lm",
        ]
    if sanitizer:
        flags.append(sanitizer)
    return flags


def _load_average() -> list[float]:
    try:
        return [float(value) for value in os.getloadavg()]
    except (AttributeError, OSError):
        return []


def _power_source() -> str:
    if sys.platform != "darwin":
        return "runner-policy"
    try:
        output = subprocess.check_output(["pmset", "-g", "batt"], text=True)
    except (OSError, subprocess.SubprocessError):
        return "unavailable"
    first = output.splitlines()[0] if output.splitlines() else ""
    return first.strip("'; ") or "unknown"


def capture_metadata(
    repository: pathlib.Path,
    ruda_binary: pathlib.Path,
    *,
    warmups: int,
    samples: int,
    timeout_seconds: int,
    max_heap_bytes: int,
    command: Sequence[str],
) -> dict[str, Any]:
    ruda_binary = ruda_binary.resolve()
    if not ruda_binary.is_file() or not os.access(ruda_binary, os.X_OK):
        raise ProtocolError(f"Ruda executable is not runnable: {ruda_binary}")
    version_lines = _version_lines(ruda_binary, repository)
    manifest_path, archive_path, runtime_manifest = locate_runtime(
        ruda_binary, version_lines
    )
    config = _build_config(ruda_binary)
    native_compiler = pathlib.Path(
        config.get("RUDA_NATIVE_C_COMPILER", os.environ.get("CC", "cc"))
    )
    if not native_compiler.is_absolute():
        resolved = shutil.which(str(native_compiler))
        if resolved:
            native_compiler = pathlib.Path(resolved)
    system = platform.system()
    platform_data = {
        "id": platform_id(),
        "system": system,
        "release": platform.release(),
        "machine": platform.machine(),
        "cpu": cpu_name(),
        "logical_cpus": os.cpu_count() or 1,
    }
    revision = "unavailable"
    for candidate in ruda_binary.parents:
        if (candidate / ".git").exists():
            revision = git_revision(candidate, repository)
            break
    native_version = native_tool_version(
        native_compiler, repository, config, system
    )
    return {
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "platform": platform_data,
        "isolation": {
            "mode": "dedicated-runner-contract",
            "load_average_at_start": _load_average(),
            "power_source": _power_source(),
            "affinity": "not-requested",
            "sample_selection": "none",
        },
        "warmups": warmups,
        "samples": samples,
        "timeout_seconds": timeout_seconds,
        "clock": "perf_counter_ns",
        "order": "rotating-balanced-v1",
        "command": shlex.join(command),
        "resource": {"max_heap_bytes": max_heap_bytes},
        "artifacts": {
            "ruda_compiler": {
                "path": str(ruda_binary),
                "sha256": sha256_file(ruda_binary),
                "revision": revision,
                "version": "\n".join(version_lines),
            },
            "runtime": {
                "path": str(archive_path.resolve()),
                "sha256": sha256_file(archive_path),
                "manifest_path": str(manifest_path.resolve()),
                "manifest_sha256": sha256_file(manifest_path),
                **runtime_manifest,
            },
            "native_c": {
                "compiler_path": str(native_compiler),
                "compiler_version": native_version,
                "linker_path": str(native_compiler),
                "linker_version": native_version,
                "output_profile": "release",
                "flags": _native_flags(config),
            },
        },
        "toolchains": {
            "python": platform.python_version(),
            "ruda": version_lines[0] if version_lines else "unknown",
            "go": tool_version(["go", "version"], repository),
            "rust": tool_version(["rustc", "--version"], repository),
        },
    }


def finish_metadata(metadata: dict[str, Any]) -> None:
    isolation = metadata.get("isolation")
    if not isinstance(isolation, dict):
        raise ProtocolError("metadata isolation owner is missing")
    isolation["load_average_at_end"] = _load_average()
