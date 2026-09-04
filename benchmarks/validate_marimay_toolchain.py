#!/usr/bin/env python3

from __future__ import annotations

import argparse
import pathlib

from marimay_toolchain import load_contract, query_version, validate_version
from perf_protocol import ProtocolError


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate mmay against the benchmark toolchain contract."
    )
    parser.add_argument("mmay", type=pathlib.Path)
    args = parser.parse_args()
    repository = pathlib.Path(__file__).resolve().parents[1]
    try:
        path, contract = load_contract(repository)
        validate_version(contract, query_version(args.mmay.resolve()))
    except ProtocolError as error:
        raise SystemExit(str(error)) from error
    print(
        "Marimay toolchain contract ok: "
        f"{contract['compiler']}; language={contract['language']}; "
        f"contract={path.relative_to(repository)}"
    )


if __name__ == "__main__":
    main()
