"""Own immutable compiler/runtime and executable copies for one catalogue run."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import tempfile

from perf_protocol import ProtocolError, sha256_file


def compiler_path(repository: Path) -> Path:
    selected = os.environ.get("MMAY")
    if selected is None:
        selected = shutil.which("mmay") or str(repository.parent / "marimay/build/release/mmay")
    return Path(selected).resolve()


def create_workspace(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="run-", dir=root)).resolve()


def _include_roots(compiler: Path) -> list[Path]:
    installed = compiler.parent.parent / "include"
    if (installed / "mmay/base/allocator.h").is_file():
        return [installed]
    config = compiler.parent / "generated/mmay/build_config.h"
    if not config.is_file():
        raise ProtocolError("cannot pin compiler headers: build config or installed include tree missing")
    values = {}
    pattern = re.compile(r'^#define MMAY_NATIVE_(BOOTSTRAP_INCLUDE|RUNTIME_INCLUDE) (".*")$')
    for line in config.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            values[match.group(1)] = Path(json.loads(match.group(2)))
    if set(values) != {"BOOTSTRAP_INCLUDE", "RUNTIME_INCLUDE"}:
        raise ProtocolError("cannot pin compiler headers: incomplete build configuration")
    return [values["BOOTSTRAP_INCLUDE"], values["RUNTIME_INCLUDE"]]


def pin_toolchain(compiler: Path, workspace: Path, metadata: dict) -> tuple[Path, dict[str, str]]:
    """Capture a coherent installed layout; never retain links to mutable inputs."""
    compiler = compiler.resolve()
    prefix = workspace / "toolchain"
    runtime = metadata["artifacts"]["runtime"]
    runtime_version = runtime["runtime"]
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", runtime_version) is None:
        raise ProtocolError("invalid runtime version in snapshot layout")
    binary = prefix / "bin" / compiler.name
    runtime_dir = prefix / "lib/mmay" / runtime_version / "native/release"
    sources = {
        binary: compiler,
        runtime_dir / Path(runtime["path"]).name: Path(runtime["path"]),
        runtime_dir / Path(runtime["manifest_path"]).name: Path(runtime["manifest_path"]),
    }
    for include in _include_roots(compiler):
        headers = sorted((include / "mmay").rglob("*.h"))
        if not headers:
            raise ProtocolError(f"cannot pin empty compiler include tree: {include}")
        for header in headers:
            target = prefix / "include" / header.relative_to(include)
            if target in sources and sha256_file(sources[target]) != sha256_file(header):
                raise ProtocolError(f"conflicting compiler snapshot header: {target.name}")
            sources[target] = header
    before = {target: sha256_file(source) for target, source in sources.items()}
    expected = {
        binary: metadata["artifacts"]["mmay_compiler"]["sha256"],
        runtime_dir / Path(runtime["path"]).name: runtime["sha256"],
        runtime_dir / Path(runtime["manifest_path"]).name: runtime["manifest_sha256"],
    }
    if any(before[path] != digest for path, digest in expected.items()):
        raise ProtocolError("compiler/runtime changed while preparing snapshot; retry")
    for target, source in sources.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for target, source in sources.items():
        if sha256_file(target) != before[target] or sha256_file(source) != before[target]:
            raise ProtocolError("compiler/runtime changed while copying snapshot; retry")
    captured = {str(target): digest for target, digest in before.items()}
    metadata["toolchain_snapshot"] = {
        "source_compiler": str(compiler),
        "source_runtime": runtime["path"],
        "source_manifest": runtime["manifest_path"],
        "directory": str(prefix),
        "files_sha256": captured,
        "standard_library": "compiler-embedded source packages",
    }
    metadata["artifacts"]["mmay_compiler"]["path"] = str(binary)
    runtime["path"] = str(runtime_dir / Path(runtime["path"]).name)
    runtime["manifest_path"] = str(runtime_dir / Path(runtime["manifest_path"]).name)
    return binary, captured


def pin_external_executables(commands: dict, workspace: Path) -> None:
    """Rust/shared build outputs may be replaced by another build after capture."""
    captured = {}
    for workloads in commands.values():
        for command in workloads.values():
            source = Path(command[0]).resolve()
            if source.is_relative_to(workspace):
                continue
            if source not in captured:
                before = sha256_file(source)
                destination = workspace / "executables" / (before + "-" + source.name)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                if sha256_file(destination) != before or sha256_file(source) != before:
                    raise ProtocolError("executable changed while copying snapshot; retry")
                captured[source] = destination
            command[0] = str(captured[source])
