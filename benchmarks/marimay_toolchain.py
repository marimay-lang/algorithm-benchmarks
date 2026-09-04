from __future__ import annotations

import json
import pathlib
import subprocess
from collections.abc import Mapping
from typing import Any

from perf_protocol import ProtocolError


CONTRACT_SCHEMA = "marimay.algorithm-toolchain/1"
CONTRACT_PATH = pathlib.Path("benchmarks/marimay-toolchain.json")
STRING_FIELDS = (
    "version_schema",
    "compiler",
    "runtime",
    "language",
    "standard_library",
)


def validate_contract(contract: Mapping[str, Any]) -> None:
    if contract.get("schema") != CONTRACT_SCHEMA:
        raise ProtocolError("unsupported Marimay toolchain contract schema")
    for field in STRING_FIELDS:
        value = contract.get(field)
        if not isinstance(value, str) or not value:
            raise ProtocolError(f"Marimay toolchain contract has invalid {field}")
    commands = contract.get("required_commands")
    if (
        not isinstance(commands, list)
        or not commands
        or any(not isinstance(command, str) or not command for command in commands)
        or len(commands) != len(set(commands))
        or commands != sorted(commands)
    ):
        raise ProtocolError(
            "Marimay toolchain required_commands must be unique sorted names"
        )


def load_contract(repository: pathlib.Path) -> tuple[pathlib.Path, dict[str, Any]]:
    path = repository / CONTRACT_PATH
    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ProtocolError(f"cannot load Marimay toolchain contract: {error}") from error
    if not isinstance(contract, dict):
        raise ProtocolError("Marimay toolchain contract must be a JSON object")
    validate_contract(contract)
    return path, contract


def validate_version(
    contract: Mapping[str, Any], version: Mapping[str, Any]
) -> None:
    actual = {
        "version_schema": version.get("schema"),
        "compiler": version.get("compiler"),
        "runtime": version.get("runtime"),
        "language": version.get("language"),
    }
    standard_library = version.get("standardLibrary")
    actual["standard_library"] = (
        standard_library.get("version")
        if isinstance(standard_library, Mapping)
        else None
    )
    for field in STRING_FIELDS:
        if actual[field] != contract[field]:
            raise ProtocolError(
                f"Marimay {field} mismatch: expected {contract[field]!r}, "
                f"got {actual[field]!r}"
            )

    commands = version.get("commands")
    available = commands.get("available") if isinstance(commands, Mapping) else None
    if not isinstance(available, list) or any(
        not isinstance(command, str) for command in available
    ):
        raise ProtocolError("Marimay version contract has invalid available commands")
    missing = sorted(set(contract["required_commands"]) - set(available))
    if missing:
        raise ProtocolError(
            "Marimay toolchain lacks required commands: " + ", ".join(missing)
        )


def query_version(mmay_binary: pathlib.Path) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            [str(mmay_binary), "version", "--json"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise ProtocolError(f"cannot query Marimay version: {error}") from error
    try:
        version = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ProtocolError("Marimay version output is not valid JSON") from error
    if not isinstance(version, dict):
        raise ProtocolError("Marimay version output must be a JSON object")
    return version


def validate_executable(repository: pathlib.Path, mmay_binary: pathlib.Path) -> None:
    _, contract = load_contract(repository)
    validate_version(contract, query_version(mmay_binary))
