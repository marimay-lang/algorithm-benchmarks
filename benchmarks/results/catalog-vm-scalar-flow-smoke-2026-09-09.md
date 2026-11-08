# Catalogue and language benchmark

Generated: 2026-09-09T14:42:10+07:00; profile: **smoke**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay VM (source run) ms |
|---|---|---|
| title-search-10k | 32 × 3 | 74.38 |
| title-search-100k | 128 × 3 | 74.73 |
| normalize-title | 32 × 3 | 75.51 |
| word-frequency | 32 × 3 | 73.59 |
| report-builder | 32 × 3 | 75.38 |
| report-concat | 32 × 3 | 75.38 |
| map-int | 32 × 3 | 74.28 |
| map-string | 32 × 3 | 74.32 |
| map-string-book | 32 × 3 | 74.14 |
| set-string-churn | 32 × 3 | 74.62 |
| catalog-match | 32 × 3 | 75.22 |
| catalog-dotcall | 32 × 3 | 76.16 |
| catalog-interface | 32 × 3 | 76.03 |
| record-reference-copy | 32 × 3 | 74.68 |
| record-create | 32 × 3 | 74.45 |
| array-grow | 32 × 3 | 75.19 |
| array-reserved | 32 × 3 | 75.13 |
| bfs-int | 32 × 3 | 74.93 |
| bfs-record | 32 × 3 | 75.25 |
| catalog-pipeline | 32 × 3 | 74.80 |
| parse-result | 32 × 3 | 74.94 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay VM (source run) | 0.40 | 2.19 | 72.60–74.79 | 3% |
| title-search-100k | Marimay VM (source run) | 0.02 | 0.67 | 74.08–74.75 | 2% |
| normalize-title | Marimay VM (source run) | 1.14 | 3.02 | 74.37–77.40 | 5% |
| word-frequency | Marimay VM (source run) | 0.34 | 2.04 | 73.25–75.29 | 3% |
| report-builder | Marimay VM (source run) | 0.64 | 1.93 | 74.74–76.67 | 3% |
| report-concat | Marimay VM (source run) | 0.10 | 1.01 | 74.47–75.48 | 2% |
| map-int | Marimay VM (source run) | 0.24 | 0.57 | 74.04–74.60 | 2% |
| map-string | Marimay VM (source run) | 0.80 | 2.32 | 73.52–75.84 | 3% |
| map-string-book | Marimay VM (source run) | 1.31 | 5.01 | 70.45–75.46 | 7% |
| set-string-churn | Marimay VM (source run) | 0.28 | 1.89 | 74.35–76.24 | 3% |
| catalog-match | Marimay VM (source run) | 2.35 | 98.62 | 72.87–171.49 | 131% |
| catalog-dotcall | Marimay VM (source run) | 2.30 | 5.09 | 73.86–78.95 | 9% |
| catalog-interface | Marimay VM (source run) | 0.86 | 100.09 | 75.17–175.26 | 132% |
| record-reference-copy | Marimay VM (source run) | 0.82 | 3.98 | 73.86–77.83 | 5% |
| record-create | Marimay VM (source run) | 0.30 | 1.25 | 74.15–75.40 | 2% |
| array-grow | Marimay VM (source run) | 0.23 | 1.33 | 74.08–75.41 | 2% |
| array-reserved | Marimay VM (source run) | 0.07 | 1.02 | 74.17–75.19 | 2% |
| bfs-int | Marimay VM (source run) | 0.53 | 1.98 | 74.40–76.38 | 3% |
| bfs-record | Marimay VM (source run) | 0.04 | 0.58 | 75.21–75.78 | 2% |
| catalog-pipeline | Marimay VM (source run) | 0.22 | 2.37 | 74.57–76.95 | 3% |
| parse-result | Marimay VM (source run) | 0.07 | 0.60 | 74.40–75.01 | 2% |

## Coverage and representations

- **title-search-10k**: Linear exact UTF-8 title search; 75% hits and 25% misses.
- **title-search-100k**: Same queries over 100,000 unique runtime-built titles.
- **normalize-title**: ASCII trim, owned scalar pieces, explicit ASCII/Russian folding table, builder, equality.
- **word-frequency**: Four-token Russian/ASCII lines; owned token split and map counts; all keys checked.
- **report-builder**: Build 10k formatted rows using a growing string builder; checksum every UTF-8 byte.
- **report-concat**: Same rows with a fresh immutable concatenation each step (quadratic copy volume).
- **map-int**: 4096 integer keys, get then put; deterministic permutation and full weighted histogram.
- **map-string**: Same map trace with dynamic Russian/ASCII title keys; fresh equal keys for final lookups.
- **map-string-book**: Dynamic string keys to Book references; construct once, lookup and read title/state/serial.
- **set-string-churn**: Sliding live window; remove old string, check absence, insert fresh key; verify final membership.
- **catalog-match**: BookState enum + exhaustive match; Go tagged struct + switch, Rust enum + match.
- **catalog-dotcall**: Concrete Book label call; no per-call result string allocation.
- **catalog-interface**: Materialized interface array; method-table call and UTF-8 label length.
- **record-reference-copy**: Retain aliases in a growing array; compare every identity and read fields.
- **record-create**: Retain fresh Book objects per batch; same fields, distinct identity; titles/states shared.
- **array-grow**: Append integers from empty capacity, then checksum all values.
- **array-reserved**: Same append trace with one initial reserve.
- **bfs-int**: Contiguous integer IDs, growing integer queue, distance array, degree 16.
- **bfs-record**: Same edges/distances; Node records and reference queue; edges remain integer IDs.
- **catalog-pipeline**: Combined title search, title frequency map, and BookState match; 25% missing queries.
- **parse-result**: Format/parse decimal tokens, 25% invalid suffixes; propagate Result/error then match.

## Interpretation limits

- No general Unicode lower/casefold API: normalize-title measures a shared corpus folding helper only.
- No I/O, concurrency, JSON or HTTP claims.
- Allocation workloads prescribe escaping objects; allocation counts, GC pauses and peak RSS are not measured.
- Map/set implementations retain host ordering, hashing, growth and GC policies. Cross-language equality is observable results, not identical runtime layouts.
- Go uses *Book and Rust Rc<Book> to preserve Marimay reference identity; Rust Rc costs do not generalize to all Rust representations.
- BFS has fixed degree 16 and contiguous IDs; it is not an O(V²)-edge dense graph and record edges are IDs, not object pointers.
- The per-workload Go targets are exploratory thresholds, not reviewed release budgets. No average score or general ‘Go parity’ verdict is computed.
- Short cases can be dominated by process startup and validation; repeat with larger documented inputs before attributing a difference to dispatch, GC or a particular primitive.
- Interface results include array construction/boxing and compiler devirtualization opportunities; they are not isolated virtual-call latency.

## Toolchains

- python: `3.9.6`
- marimay: `Marimay compiler 0.1.0-alpha.1`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Command: `./benchmarks/catalog_bench.py --engine vm --profile smoke --verify-only --samples 3 --warmups 0 --output benchmarks/results/catalog-vm-scalar-flow-smoke-2026-09-09.md`
