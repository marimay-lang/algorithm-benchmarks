# Privacy transformation of historical benchmark evidence

On 2026-11-08, preparation for public hosting replaced personal checkout
prefixes and private service addresses in historical reports with example
locations. These are **privacy-transformed historical reports**, not fresh
measurements or byte-identical copies of the original receipts. Paths such as
`/home/marimay/` are placeholders, not measured machine locations or instructions
to use that directory.

The original complete files and Git histories remain in the maintainer's
private filesystem archive. That archive is not a publication target. Its
original checksums remain useful for comparing the private originals; checksums
for the public reports identify the transformed bytes instead.

## Checkpoint-21 macOS baseline receipt bindings

The two baseline reports below changed only in path strings: 12 fields in the
probe report and 27 fields in the algorithm report. A structural comparison
against their original committed JSON verified that every changed leaf was
the personal-home-prefix replacement. Every other JSON value was identical,
including raw timing samples, summaries, resource limits, output checksums,
source/manifest/compiler/runtime hashes, revision IDs, and measurement dates.

| Report | Original SHA-256 | Public transformed SHA-256 |
| --- | --- | --- |
| `cp21-probes-macos-arm64-apple-m2.json` | `0b42347540795d6ea2605597666a8318dfef6f4b78864a5c630a541e88817180` | `e80c9272ec3b7c532f996a6e9d61feb14009d070268a7631a325cacb64d52184` |
| `cp21-algorithms-macos-arm64-apple-m2.json` | `818969be79d7fb3ca7e1fcd1fe8ac18b4dca2ceab541ae5c033848e024134081` | `d8083659f0f9e52760cf7c29e2c6576e8b0b3583f22c3f072b04aa650d48fd67` |

Only `baseline.probe_result_sha256` and
`baseline.algorithm_result_sha256` in
[`../budgets/cp21-macos-arm64-apple-m2.json`](../budgets/cp21-macos-arm64-apple-m2.json)
were rebound to those public file bytes. The reviewed budget values,
historical review metadata, measured results, and all artifact/source identity
fields remain unchanged. This does not claim that the historical reviewer
reviewed the later privacy transformation.

The Linux baseline bytes and their receipt bindings did not change. No
validator was relaxed: exact repository-relative paths, file SHA-256 bindings,
protocol compatibility, source identity, and budget checks remain required.

The focused Tier 1 registry test and the full Python suite must pass against
the public working tree. Passing these receipt checks confirms internal
consistency of the transformed reports; it does not re-run the original
benchmarks, establish a new performance baseline, or complete the remaining
public-alpha platform matrix.
