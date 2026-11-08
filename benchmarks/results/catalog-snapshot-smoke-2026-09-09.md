# Catalogue and language benchmark

Generated: 2026-09-09T15:35:48+07:00; profile: **smoke**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | Marimay VM (source run) ms |
|---|---|---|---|---|---|
| title-search-10k | 32 × 3 | 3.26 | 3.31 | 3.15 | 70.38 |
| title-search-100k | 128 × 3 | 3.09 | 3.16 | 3.05 | 70.22 |
| normalize-title | 32 × 3 | 3.52 | 3.10 | 2.72 | 71.38 |
| word-frequency | 32 × 3 | 2.77 | 2.93 | 2.53 | 70.31 |
| report-builder | 32 × 3 | 3.28 | 3.05 | 2.45 | 71.24 |
| report-concat | 32 × 3 | 3.30 | 3.17 | 3.04 | 70.78 |
| map-int | 32 × 3 | 3.02 | 3.26 | 2.50 | 69.78 |
| map-string | 32 × 3 | 2.54 | 2.96 | 2.55 | 70.42 |
| map-string-book | 32 × 3 | 3.24 | 3.24 | 2.65 | 70.62 |
| set-string-churn | 32 × 3 | 3.27 | 3.19 | 3.16 | 70.31 |
| catalog-match | 32 × 3 | 3.11 | 3.13 | 2.51 | 70.17 |
| catalog-dotcall | 32 × 3 | 2.34 | 2.95 | 2.62 | 69.81 |
| catalog-interface | 32 × 3 | 3.07 | 3.33 | 2.59 | 70.47 |
| record-reference-copy | 32 × 3 | 3.14 | 3.09 | 3.09 | 70.54 |
| record-create | 32 × 3 | 3.05 | 3.11 | 2.49 | 70.03 |
| array-grow | 32 × 3 | 2.58 | 3.03 | 2.64 | 69.88 |
| array-reserved | 32 × 3 | 3.06 | 3.11 | 2.61 | 70.08 |
| bfs-int | 32 × 3 | 3.28 | 3.16 | 3.16 | 71.06 |
| bfs-record | 32 × 3 | 3.06 | 3.15 | 2.59 | 70.47 |
| catalog-pipeline | 32 × 3 | 2.54 | 3.06 | 2.51 | 70.46 |
| parse-result | 32 × 3 | 2.94 | 3.07 | 2.57 | 69.88 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.20 | 375.72 | 3.06–378.78 | 11525% |
| title-search-10k | Go native | 0.22 | 385.69 | 3.09–388.78 | 11661% |
| title-search-10k | Rust native | 0.06 | 366.06 | 3.09–369.15 | 11622% |
| title-search-10k | Marimay VM (source run) | 0.66 | 20.74 | 69.72–90.46 | 29% |
| title-search-100k | Marimay native | 0.05 | 0.14 | 3.03–3.17 | 5% |
| title-search-100k | Go native | 0.07 | 0.24 | 3.10–3.33 | 7% |
| title-search-100k | Rust native | 0.10 | 0.23 | 2.95–3.18 | 10% |
| title-search-100k | Marimay VM (source run) | 0.71 | 1.43 | 69.49–70.92 | 3% |
| normalize-title | Marimay native | 0.05 | 0.41 | 3.47–3.89 | 12% |
| normalize-title | Go native | 0.02 | 0.15 | 3.08–3.23 | 5% |
| normalize-title | Rust native | 0.01 | 0.19 | 2.72–2.91 | 7% |
| normalize-title | Marimay VM (source run) | 0.51 | 1.15 | 70.87–72.02 | 2% |
| word-frequency | Marimay native | 0.13 | 0.41 | 2.48–2.90 | 15% |
| word-frequency | Go native | 0.09 | 0.21 | 2.84–3.05 | 9% |
| word-frequency | Rust native | 0.05 | 0.12 | 2.46–2.58 | 6% |
| word-frequency | Marimay VM (source run) | 0.10 | 1.12 | 69.28–70.40 | 2% |
| report-builder | Marimay native | 0.11 | 0.27 | 3.12–3.39 | 10% |
| report-builder | Go native | 0.02 | 0.12 | 3.04–3.16 | 4% |
| report-builder | Rust native | 0.02 | 0.22 | 2.43–2.65 | 9% |
| report-builder | Marimay VM (source run) | 0.64 | 1.42 | 70.47–71.88 | 3% |
| report-concat | Marimay native | 0.07 | 0.30 | 3.07–3.37 | 9% |
| report-concat | Go native | 0.00 | 0.04 | 3.16–3.21 | 2% |
| report-concat | Rust native | 0.00 | 0.07 | 3.04–3.11 | 2% |
| report-concat | Marimay VM (source run) | 0.35 | 1.86 | 70.44–72.29 | 3% |
| map-int | Marimay native | 0.10 | 0.45 | 2.92–3.37 | 15% |
| map-int | Go native | 0.19 | 0.46 | 3.07–3.52 | 18% |
| map-int | Rust native | 0.06 | 0.20 | 2.36–2.56 | 8% |
| map-int | Marimay VM (source run) | 0.03 | 0.22 | 69.75–69.98 | 2% |
| map-string | Marimay native | 0.07 | 0.28 | 2.47–2.75 | 11% |
| map-string | Go native | 0.01 | 0.29 | 2.96–3.25 | 10% |
| map-string | Rust native | 0.02 | 0.27 | 2.53–2.80 | 11% |
| map-string | Marimay VM (source run) | 0.33 | 1.08 | 70.09–71.16 | 2% |
| map-string-book | Marimay native | 0.02 | 0.20 | 3.07–3.26 | 6% |
| map-string-book | Go native | 0.04 | 0.20 | 3.08–3.28 | 6% |
| map-string-book | Rust native | 0.02 | 0.14 | 2.53–2.67 | 5% |
| map-string-book | Marimay VM (source run) | 0.02 | 0.46 | 70.18–70.64 | 2% |
| set-string-churn | Marimay native | 0.08 | 0.40 | 2.95–3.35 | 12% |
| set-string-churn | Go native | 0.01 | 0.35 | 3.18–3.53 | 11% |
| set-string-churn | Rust native | 0.07 | 0.16 | 3.07–3.23 | 7% |
| set-string-churn | Marimay VM (source run) | 0.21 | 1.12 | 70.11–71.22 | 2% |
| catalog-match | Marimay native | 0.05 | 0.13 | 3.03–3.16 | 5% |
| catalog-match | Go native | 0.02 | 0.48 | 3.11–3.59 | 15% |
| catalog-match | Rust native | 0.10 | 0.43 | 2.41–2.84 | 17% |
| catalog-match | Marimay VM (source run) | 0.33 | 0.76 | 69.74–70.50 | 2% |
| catalog-dotcall | Marimay native | 0.01 | 0.06 | 2.33–2.39 | 2% |
| catalog-dotcall | Go native | 0.13 | 0.38 | 2.82–3.19 | 13% |
| catalog-dotcall | Rust native | 0.07 | 0.29 | 2.40–2.69 | 11% |
| catalog-dotcall | Marimay VM (source run) | 0.13 | 0.29 | 69.68–69.96 | 2% |
| catalog-interface | Marimay native | 0.12 | 0.27 | 2.92–3.19 | 12% |
| catalog-interface | Go native | 0.22 | 0.58 | 3.11–3.69 | 20% |
| catalog-interface | Rust native | 0.09 | 1.30 | 2.50–3.80 | 50% |
| catalog-interface | Marimay VM (source run) | 0.53 | 1.07 | 69.94–71.01 | 2% |
| record-reference-copy | Marimay native | 0.15 | 0.34 | 2.95–3.29 | 14% |
| record-reference-copy | Go native | 0.04 | 0.20 | 3.05–3.25 | 6% |
| record-reference-copy | Rust native | 0.07 | 0.20 | 2.96–3.16 | 7% |
| record-reference-copy | Marimay VM (source run) | 0.42 | 0.88 | 70.12–71.01 | 2% |
| record-create | Marimay native | 0.14 | 0.29 | 2.90–3.19 | 13% |
| record-create | Go native | 0.04 | 0.09 | 3.06–3.15 | 4% |
| record-create | Rust native | 0.04 | 0.09 | 2.45–2.54 | 4% |
| record-create | Marimay VM (source run) | 0.22 | 0.61 | 69.64–70.25 | 2% |
| array-grow | Marimay native | 0.03 | 0.19 | 2.55–2.74 | 7% |
| array-grow | Go native | 0.12 | 0.39 | 2.91–3.30 | 13% |
| array-grow | Rust native | 0.02 | 0.12 | 2.54–2.66 | 5% |
| array-grow | Marimay VM (source run) | 0.01 | 2.45 | 69.87–72.33 | 4% |
| array-reserved | Marimay native | 0.26 | 0.53 | 2.79–3.32 | 26% |
| array-reserved | Go native | 0.02 | 0.06 | 3.07–3.14 | 2% |
| array-reserved | Rust native | 0.01 | 0.11 | 2.51–2.62 | 4% |
| array-reserved | Marimay VM (source run) | 0.03 | 0.25 | 70.04–70.29 | 2% |
| bfs-int | Marimay native | 0.24 | 0.55 | 2.97–3.52 | 22% |
| bfs-int | Go native | 0.02 | 0.10 | 3.15–3.25 | 3% |
| bfs-int | Rust native | 0.18 | 0.48 | 2.86–3.35 | 17% |
| bfs-int | Marimay VM (source run) | 0.65 | 1.44 | 70.27–71.71 | 3% |
| bfs-record | Marimay native | 0.10 | 0.48 | 2.96–3.44 | 16% |
| bfs-record | Go native | 0.04 | 0.09 | 3.11–3.19 | 4% |
| bfs-record | Rust native | 0.02 | 0.07 | 2.57–2.64 | 3% |
| bfs-record | Marimay VM (source run) | 0.62 | 1.25 | 69.83–71.09 | 3% |
| catalog-pipeline | Marimay native | 0.08 | 0.17 | 2.45–2.62 | 10% |
| catalog-pipeline | Go native | 0.02 | 0.22 | 2.87–3.09 | 7% |
| catalog-pipeline | Rust native | 0.10 | 0.20 | 2.42–2.61 | 12% |
| catalog-pipeline | Marimay VM (source run) | 0.30 | 0.72 | 70.16–70.88 | 2% |
| parse-result | Marimay native | 0.06 | 0.19 | 2.88–3.07 | 6% |
| parse-result | Go native | 0.05 | 0.46 | 3.03–3.48 | 15% |
| parse-result | Rust native | 0.01 | 0.07 | 2.51–2.58 | 3% |
| parse-result | Marimay VM (source run) | 0.46 | 1.14 | 69.42–70.56 | 2% |

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

Command: `benchmarks/catalog_bench.py --profile smoke --engine both --verify-only --output benchmarks/results/catalog-snapshot-smoke-2026-09-09.md`
