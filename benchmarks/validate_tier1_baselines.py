#!/usr/bin/env python3

from __future__ import annotations

import pathlib

from perf_protocol import ProtocolError
from tier1_baselines import validate_tier1_registry


def main() -> None:
    repository = pathlib.Path(__file__).resolve().parents[1]
    count, targets = validate_tier1_registry(repository)
    print(
        f"checkpoint-21 Tier 1 registry valid: {count} reviewed baselines "
        f"({', '.join(targets)})"
    )


if __name__ == "__main__":
    try:
        main()
    except (ProtocolError, KeyError, TypeError) as error:
        raise SystemExit(f"Tier 1 baseline validation error: {error}") from error
