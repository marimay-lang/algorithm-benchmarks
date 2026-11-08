# Catalogue and language benchmark

Generated: 2026-09-09T15:36:29+07:00; profile: **smoke**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | Marimay VM (source run) ms |
|---|---|---|---|---|---|
| title-search-10k | 32 × 3 | 3.36 | 3.57 | 3.35 | 70.93 |
| title-search-100k | 128 × 3 | 3.23 | 3.15 | 2.97 | 69.76 |
| normalize-title | 32 × 3 | 3.62 | 3.29 | 2.66 | 71.24 |
| word-frequency | 32 × 3 | 2.62 | 3.09 | 2.64 | 70.31 |
| report-builder | 32 × 3 | 3.14 | 3.25 | 2.62 | 70.82 |
| report-concat | 32 × 3 | 2.94 | 3.28 | 3.18 | 71.04 |
| map-int | 32 × 3 | 3.15 | 3.35 | 2.62 | 70.25 |
| map-string | 32 × 3 | 2.53 | 3.00 | 2.69 | 70.56 |
| map-string-book | 32 × 3 | 3.26 | 3.28 | 2.60 | 70.42 |
| set-string-churn | 32 × 3 | 3.29 | 3.30 | 3.45 | 70.60 |
| catalog-match | 32 × 3 | 2.90 | 3.39 | 2.54 | 70.62 |
| catalog-dotcall | 32 × 3 | 2.42 | 3.01 | 2.66 | 69.59 |
| catalog-interface | 32 × 3 | 2.97 | 3.23 | 2.54 | 69.97 |
| record-reference-copy | 32 × 3 | 2.91 | 3.44 | 3.07 | 70.09 |
| record-create | 32 × 3 | 3.15 | 3.27 | 2.60 | 70.03 |
| array-grow | 32 × 3 | 2.36 | 2.97 | 2.64 | 69.72 |
| array-reserved | 32 × 3 | 2.96 | 3.35 | 2.57 | 69.70 |
| bfs-int | 32 × 3 | 2.96 | 3.24 | 3.20 | 70.36 |
| bfs-record | 32 × 3 | 3.06 | 3.24 | 2.67 | 70.32 |
| catalog-pipeline | 32 × 3 | 2.37 | 3.07 | 2.72 | 70.74 |
| parse-result | 32 × 3 | 3.10 | 3.23 | 2.63 | 70.66 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.12 | 246.11 | 3.24–249.35 | 7329% |
| title-search-10k | Go native | 0.44 | 232.89 | 3.12–236.01 | 6530% |
| title-search-10k | Rust native | 0.32 | 221.09 | 3.03–224.12 | 6605% |
| title-search-10k | Marimay VM (source run) | 1.09 | 29.64 | 69.84–99.47 | 42% |
| title-search-100k | Marimay native | 0.21 | 0.46 | 3.02–3.48 | 20% |
| title-search-100k | Go native | 0.02 | 0.11 | 3.13–3.24 | 4% |
| title-search-100k | Rust native | 0.06 | 0.42 | 2.61–3.03 | 14% |
| title-search-100k | Marimay VM (source run) | 0.04 | 0.42 | 69.72–70.13 | 2% |
| normalize-title | Marimay native | 0.14 | 0.39 | 3.48–3.87 | 12% |
| normalize-title | Go native | 0.13 | 0.26 | 3.16–3.42 | 12% |
| normalize-title | Rust native | 0.05 | 0.32 | 2.60–2.93 | 12% |
| normalize-title | Marimay VM (source run) | 0.00 | 0.26 | 71.24–71.50 | 2% |
| word-frequency | Marimay native | 0.00 | 0.02 | 2.61–2.62 | 2% |
| word-frequency | Go native | 0.03 | 0.07 | 3.05–3.12 | 3% |
| word-frequency | Rust native | 0.02 | 0.06 | 2.61–2.67 | 3% |
| word-frequency | Marimay VM (source run) | 0.11 | 0.48 | 69.94–70.42 | 2% |
| report-builder | Marimay native | 0.02 | 0.18 | 3.12–3.30 | 6% |
| report-builder | Go native | 0.13 | 0.35 | 3.12–3.47 | 12% |
| report-builder | Rust native | 0.04 | 0.17 | 2.58–2.75 | 7% |
| report-builder | Marimay VM (source run) | 0.03 | 0.09 | 70.79–70.87 | 2% |
| report-concat | Marimay native | 0.02 | 0.15 | 2.92–3.07 | 5% |
| report-concat | Go native | 0.00 | 0.06 | 3.23–3.29 | 2% |
| report-concat | Rust native | 0.01 | 0.03 | 3.17–3.20 | 2% |
| report-concat | Marimay VM (source run) | 0.47 | 1.02 | 70.57–71.59 | 2% |
| map-int | Marimay native | 0.30 | 0.64 | 2.81–3.45 | 29% |
| map-int | Go native | 0.14 | 0.40 | 3.09–3.49 | 13% |
| map-int | Rust native | 0.00 | 0.05 | 2.58–2.63 | 2% |
| map-int | Marimay VM (source run) | 0.28 | 0.74 | 69.79–70.52 | 2% |
| map-string | Marimay native | 0.02 | 0.05 | 2.50–2.55 | 2% |
| map-string | Go native | 0.00 | 0.02 | 3.00–3.02 | 2% |
| map-string | Rust native | 0.03 | 0.07 | 2.67–2.74 | 3% |
| map-string | Marimay VM (source run) | 0.22 | 0.74 | 70.05–70.78 | 2% |
| map-string-book | Marimay native | 0.05 | 0.20 | 3.12–3.31 | 6% |
| map-string-book | Go native | 0.04 | 0.43 | 3.24–3.66 | 13% |
| map-string-book | Rust native | 0.02 | 0.29 | 2.58–2.87 | 11% |
| map-string-book | Marimay VM (source run) | 0.54 | 1.15 | 69.87–71.02 | 2% |
| set-string-churn | Marimay native | 0.02 | 0.06 | 3.27–3.32 | 2% |
| set-string-churn | Go native | 0.08 | 0.26 | 3.12–3.38 | 8% |
| set-string-churn | Rust native | 0.04 | 0.46 | 3.03–3.48 | 13% |
| set-string-churn | Marimay VM (source run) | 0.30 | 0.80 | 70.10–70.90 | 2% |
| catalog-match | Marimay native | 0.09 | 0.24 | 2.81–3.05 | 9% |
| catalog-match | Go native | 0.06 | 0.29 | 3.16–3.44 | 9% |
| catalog-match | Rust native | 0.06 | 0.13 | 2.48–2.61 | 7% |
| catalog-match | Marimay VM (source run) | 0.20 | 0.81 | 70.01–70.82 | 2% |
| catalog-dotcall | Marimay native | 0.03 | 0.21 | 2.39–2.60 | 9% |
| catalog-dotcall | Go native | 0.10 | 0.21 | 2.91–3.12 | 10% |
| catalog-dotcall | Rust native | 0.04 | 0.11 | 2.58–2.70 | 4% |
| catalog-dotcall | Marimay VM (source run) | 0.01 | 0.47 | 69.59–70.06 | 2% |
| catalog-interface | Marimay native | 0.01 | 0.19 | 2.80–2.98 | 6% |
| catalog-interface | Go native | 0.07 | 0.15 | 3.17–3.32 | 6% |
| catalog-interface | Rust native | 0.09 | 0.19 | 2.44–2.63 | 10% |
| catalog-interface | Marimay VM (source run) | 0.01 | 0.13 | 69.85–69.98 | 2% |
| record-reference-copy | Marimay native | 0.09 | 0.23 | 2.81–3.04 | 9% |
| record-reference-copy | Go native | 0.02 | 0.23 | 3.24–3.47 | 7% |
| record-reference-copy | Rust native | 0.11 | 0.46 | 2.96–3.42 | 15% |
| record-reference-copy | Marimay VM (source run) | 0.19 | 0.50 | 69.90–70.40 | 2% |
| record-create | Marimay native | 0.04 | 0.33 | 2.86–3.19 | 10% |
| record-create | Go native | 0.05 | 0.13 | 3.19–3.33 | 5% |
| record-create | Rust native | 0.04 | 0.20 | 2.44–2.64 | 8% |
| record-create | Marimay VM (source run) | 0.01 | 0.44 | 70.03–70.47 | 2% |
| array-grow | Marimay native | 0.04 | 0.12 | 2.32–2.44 | 6% |
| array-grow | Go native | 0.05 | 0.17 | 2.85–3.02 | 6% |
| array-grow | Rust native | 0.05 | 0.11 | 2.58–2.69 | 6% |
| array-grow | Marimay VM (source run) | 0.04 | 0.16 | 69.68–69.84 | 2% |
| array-reserved | Marimay native | 0.07 | 0.27 | 2.76–3.03 | 9% |
| array-reserved | Go native | 0.05 | 0.22 | 3.18–3.40 | 6% |
| array-reserved | Rust native | 0.01 | 0.04 | 2.56–2.60 | 2% |
| array-reserved | Marimay VM (source run) | 0.06 | 0.25 | 69.64–69.89 | 2% |
| bfs-int | Marimay native | 0.06 | 0.21 | 2.90–3.12 | 7% |
| bfs-int | Go native | 0.01 | 0.02 | 3.23–3.25 | 2% |
| bfs-int | Rust native | 0.04 | 0.54 | 3.16–3.70 | 17% |
| bfs-int | Marimay VM (source run) | 0.18 | 0.80 | 70.18–70.98 | 2% |
| bfs-record | Marimay native | 0.14 | 0.33 | 2.86–3.20 | 14% |
| bfs-record | Go native | 0.04 | 0.22 | 3.20–3.41 | 7% |
| bfs-record | Rust native | 0.05 | 0.20 | 2.52–2.72 | 7% |
| bfs-record | Marimay VM (source run) | 0.19 | 0.50 | 70.02–70.51 | 2% |
| catalog-pipeline | Marimay native | 0.02 | 0.16 | 2.35–2.51 | 7% |
| catalog-pipeline | Go native | 0.02 | 0.13 | 2.97–3.10 | 4% |
| catalog-pipeline | Rust native | 0.02 | 0.14 | 2.59–2.74 | 5% |
| catalog-pipeline | Marimay VM (source run) | 0.15 | 0.78 | 70.59–71.37 | 2% |
| parse-result | Marimay native | 0.05 | 0.48 | 3.05–3.53 | 16% |
| parse-result | Go native | 0.04 | 0.20 | 3.19–3.40 | 6% |
| parse-result | Rust native | 0.14 | 0.30 | 2.50–2.79 | 16% |
| parse-result | Marimay VM (source run) | 0.11 | 0.32 | 70.45–70.77 | 2% |

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

Command: `benchmarks/catalog_bench.py --profile smoke --engine both --verify-only --output /path/to/Marimay/algorithm-benchmarks/benchmarks/results/catalog-snapshot-origin-replaced-2026-09-09.md`
