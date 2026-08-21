#!/usr/bin/env python3

from __future__ import annotations

import pathlib

from equivalence import EquivalenceError, load_and_validate, manifest_sha256


def main() -> int:
    repository = pathlib.Path(__file__).resolve().parents[1]
    try:
        manifest_path, manifest = load_and_validate(repository)
    except EquivalenceError as error:
        print(f"equivalence validation failed: {error}")
        return 1
    print(
        f"equivalence manifest ok: {len(manifest['workloads'])} workloads; "
        f"sha256={manifest_sha256(manifest_path)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
