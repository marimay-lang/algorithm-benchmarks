"""Bun runtime selection and immutable capture for the catalogue matrix."""
from __future__ import annotations

import os
from pathlib import Path
import shutil

from perf_environment import run_checked
from perf_protocol import ProtocolError, sha256_file


def bun_path() -> Path:
    selected = os.environ.get("BUN") or shutil.which("bun")
    if not selected:
        raise ProtocolError("Bun not found: install Bun or set BUN=/absolute/path/to/bun; --engine native/vm excludes Bun")
    path = Path(selected).expanduser().resolve()
    if not path.is_file() or not os.access(path, os.X_OK):
        raise ProtocolError(f"Bun executable not found: {path}")
    return path


def pin_bun(source: Path, workspace: Path, metadata: dict) -> Path:
    before = sha256_file(source)
    destination = workspace / "bun/bin/bun"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if sha256_file(source) != before or sha256_file(destination) != before:
        raise ProtocolError("Bun changed while copying snapshot; retry")
    version = run_checked([str(destination), "--version"], cwd=workspace).stdout.strip()
    metadata["toolchains"]["bun"] = version
    metadata["bun_runtime"] = {
        "source": str(source), "path": str(destination), "sha256": before,
        "version": version, "engine": "JavaScriptCore JIT",
        "flags": ["--no-env-file", "--no-install", "run"],
        "environment_overrides": {
            key: value for key, value in sorted(os.environ.items())
            if key.startswith(("BUN_JSC_", "JSC_"))
            or key in ("BUN_OPTIONS", "NODE_OPTIONS", "BUN_RUNTIME_TRANSPILER_CACHE_PATH", "BUN_DEBUG_QUIET_LOGS")
        },
    }
    return destination


def bun_command(runtime: Path, entrypoint: Path) -> list[str]:
    return [str(runtime), "--no-env-file", "--no-install", "run", str(entrypoint)]
