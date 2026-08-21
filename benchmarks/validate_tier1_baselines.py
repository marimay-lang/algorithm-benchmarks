#!/usr/bin/env python3

from __future__ import annotations

import argparse
import pathlib

from perf_protocol import ProtocolError
from tier1_baselines import (
    CHECKPOINT_21_GATE,
    PUBLIC_ALPHA_GATE,
    validate_tier1_registry,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate reviewed performance baselines for one release gate."
    )
    parser.add_argument(
        "--gate",
        choices=(CHECKPOINT_21_GATE, PUBLIC_ALPHA_GATE),
        default=CHECKPOINT_21_GATE,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repository = pathlib.Path(__file__).resolve().parents[1]
    count, targets = validate_tier1_registry(repository, gate=args.gate)
    print(
        f"{args.gate} performance registry valid: {count} reviewed baselines "
        f"({', '.join(targets)})"
    )


if __name__ == "__main__":
    try:
        main()
    except (ProtocolError, KeyError, TypeError) as error:
        raise SystemExit(f"performance baseline validation error: {error}") from error
