# Catalogue and language benchmark

Generated: 2026-09-09T15:57:15+07:00; profile: **smoke**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | Marimay VM (source run) ms |
|---|---|---|---|---|---|
| title-search-10k | 32 × 3 | 2.75 | 2.99 | 2.88 | 69.04 |
| title-search-100k | 128 × 3 | 2.64 | 3.06 | 2.70 | 68.44 |
| normalize-title | 32 × 3 | 3.24 | 3.08 | 2.56 | 70.04 |
| word-frequency | 32 × 3 | 2.55 | 2.87 | 2.52 | 68.83 |
| report-builder | 32 × 3 | 2.73 | 3.00 | 2.44 | 69.50 |
| report-concat | 32 × 3 | 2.76 | 3.01 | 2.78 | 69.65 |
| map-int | 32 × 3 | 2.62 | 2.98 | 2.49 | 68.62 |
| map-string | 32 × 3 | 2.34 | 2.83 | 2.44 | 68.86 |
| map-string-book | 32 × 3 | 2.71 | 3.01 | 2.54 | 68.80 |
| set-string-churn | 32 × 3 | 2.80 | 2.98 | 2.75 | 68.95 |
| catalog-match | 32 × 3 | 2.61 | 2.98 | 2.48 | 68.60 |
| catalog-dotcall | 32 × 3 | 2.36 | 2.91 | 2.44 | 68.68 |
| catalog-interface | 32 × 3 | 2.59 | 2.95 | 2.45 | 68.86 |
| record-reference-copy | 32 × 3 | 2.58 | 2.99 | 2.73 | 68.74 |
| record-create | 32 × 3 | 2.62 | 2.91 | 2.49 | 68.83 |
| array-grow | 32 × 3 | 2.28 | 2.92 | 2.46 | 68.69 |
| array-reserved | 32 × 3 | 2.54 | 2.92 | 2.48 | 68.50 |
| bfs-int | 32 × 3 | 2.64 | 3.01 | 2.71 | 68.89 |
| bfs-record | 32 × 3 | 2.66 | 2.99 | 2.51 | 69.10 |
| catalog-pipeline | 32 × 3 | 2.40 | 2.93 | 2.56 | 69.27 |
| parse-result | 32 × 3 | 2.60 | 2.98 | 2.46 | 68.59 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.10 | 384.52 | 2.65–387.17 | 13980% |
| title-search-10k | Go native | 0.01 | 393.92 | 2.98–396.90 | 13186% |
| title-search-10k | Rust native | 0.18 | 375.01 | 2.70–377.71 | 13020% |
| title-search-10k | Marimay VM (source run) | 0.34 | 29.10 | 68.70–97.80 | 42% |
| title-search-100k | Marimay native | 0.03 | 0.38 | 2.61–2.98 | 14% |
| title-search-100k | Go native | 0.03 | 0.10 | 2.98–3.09 | 3% |
| title-search-100k | Rust native | 0.03 | 0.31 | 2.43–2.73 | 11% |
| title-search-100k | Marimay VM (source run) | 0.16 | 0.83 | 67.77–68.60 | 2% |
| normalize-title | Marimay native | 0.02 | 0.06 | 3.20–3.26 | 2% |
| normalize-title | Go native | 0.04 | 0.12 | 3.04–3.16 | 4% |
| normalize-title | Rust native | 0.07 | 0.25 | 2.49–2.74 | 10% |
| normalize-title | Marimay VM (source run) | 0.11 | 0.48 | 69.67–70.15 | 2% |
| word-frequency | Marimay native | 0.01 | 0.02 | 2.54–2.56 | 2% |
| word-frequency | Go native | 0.04 | 0.16 | 2.84–3.00 | 6% |
| word-frequency | Rust native | 0.01 | 0.03 | 2.50–2.53 | 2% |
| word-frequency | Marimay VM (source run) | 0.15 | 0.34 | 68.68–69.02 | 2% |
| report-builder | Marimay native | 0.02 | 0.09 | 2.66–2.75 | 3% |
| report-builder | Go native | 0.03 | 0.08 | 2.97–3.05 | 3% |
| report-builder | Rust native | 0.03 | 0.11 | 2.42–2.52 | 4% |
| report-builder | Marimay VM (source run) | 0.03 | 0.16 | 69.38–69.53 | 2% |
| report-concat | Marimay native | 0.01 | 0.10 | 2.76–2.86 | 4% |
| report-concat | Go native | 0.00 | 0.03 | 3.00–3.03 | 2% |
| report-concat | Rust native | 0.00 | 0.01 | 2.77–2.78 | 2% |
| report-concat | Marimay VM (source run) | 0.11 | 0.29 | 69.47–69.77 | 2% |
| map-int | Marimay native | 0.03 | 0.13 | 2.52–2.65 | 5% |
| map-int | Go native | 0.02 | 0.10 | 2.90–3.00 | 3% |
| map-int | Rust native | 0.02 | 0.09 | 2.47–2.56 | 3% |
| map-int | Marimay VM (source run) | 0.05 | 0.12 | 68.54–68.67 | 2% |
| map-string | Marimay native | 0.01 | 0.08 | 2.33–2.42 | 4% |
| map-string | Go native | 0.01 | 0.05 | 2.81–2.87 | 2% |
| map-string | Rust native | 0.03 | 0.05 | 2.41–2.46 | 3% |
| map-string | Marimay VM (source run) | 0.19 | 1.18 | 68.67–69.85 | 2% |
| map-string-book | Marimay native | 0.03 | 0.19 | 2.68–2.87 | 7% |
| map-string-book | Go native | 0.03 | 0.07 | 2.98–3.05 | 3% |
| map-string-book | Rust native | 0.03 | 0.07 | 2.50–2.57 | 4% |
| map-string-book | Marimay VM (source run) | 0.01 | 0.13 | 68.79–68.92 | 2% |
| set-string-churn | Marimay native | 0.00 | 0.01 | 2.80–2.81 | 2% |
| set-string-churn | Go native | 0.00 | 0.05 | 2.98–3.03 | 2% |
| set-string-churn | Rust native | 0.00 | 0.12 | 2.75–2.86 | 4% |
| set-string-churn | Marimay VM (source run) | 0.04 | 0.10 | 68.89–68.99 | 2% |
| catalog-match | Marimay native | 0.01 | 0.05 | 2.57–2.62 | 2% |
| catalog-match | Go native | 0.03 | 0.12 | 2.95–3.07 | 4% |
| catalog-match | Rust native | 0.03 | 0.07 | 2.44–2.51 | 4% |
| catalog-match | Marimay VM (source run) | 0.13 | 0.38 | 68.47–68.85 | 2% |
| catalog-dotcall | Marimay native | 0.01 | 0.06 | 2.35–2.42 | 3% |
| catalog-dotcall | Go native | 0.07 | 0.14 | 2.84–2.98 | 7% |
| catalog-dotcall | Rust native | 0.00 | 0.09 | 2.44–2.53 | 4% |
| catalog-dotcall | Marimay VM (source run) | 0.07 | 0.25 | 68.61–68.86 | 2% |
| catalog-interface | Marimay native | 0.01 | 0.05 | 2.58–2.63 | 2% |
| catalog-interface | Go native | 0.01 | 0.08 | 2.89–2.97 | 3% |
| catalog-interface | Rust native | 0.03 | 0.08 | 2.41–2.49 | 4% |
| catalog-interface | Marimay VM (source run) | 0.02 | 0.22 | 68.66–68.88 | 2% |
| record-reference-copy | Marimay native | 0.03 | 0.09 | 2.54–2.63 | 4% |
| record-reference-copy | Go native | 0.03 | 0.07 | 2.96–3.04 | 3% |
| record-reference-copy | Rust native | 0.04 | 0.11 | 2.66–2.76 | 4% |
| record-reference-copy | Marimay VM (source run) | 0.02 | 0.32 | 68.43–68.76 | 2% |
| record-create | Marimay native | 0.02 | 0.09 | 2.55–2.65 | 3% |
| record-create | Go native | 0.00 | 0.08 | 2.91–2.99 | 3% |
| record-create | Rust native | 0.02 | 0.13 | 2.39–2.51 | 5% |
| record-create | Marimay VM (source run) | 0.14 | 0.33 | 68.70–69.03 | 2% |
| array-grow | Marimay native | 0.02 | 0.18 | 2.27–2.45 | 8% |
| array-grow | Go native | 0.02 | 0.11 | 2.84–2.95 | 4% |
| array-grow | Rust native | 0.03 | 0.10 | 2.43–2.53 | 4% |
| array-grow | Marimay VM (source run) | 0.07 | 0.24 | 68.52–68.76 | 2% |
| array-reserved | Marimay native | 0.00 | 0.01 | 2.54–2.55 | 2% |
| array-reserved | Go native | 0.02 | 0.09 | 2.85–2.94 | 3% |
| array-reserved | Rust native | 0.03 | 0.21 | 2.45–2.65 | 8% |
| array-reserved | Marimay VM (source run) | 0.12 | 1.45 | 68.38–69.84 | 2% |
| bfs-int | Marimay native | 0.11 | 0.59 | 2.53–3.11 | 22% |
| bfs-int | Go native | 0.03 | 0.13 | 2.91–3.04 | 4% |
| bfs-int | Rust native | 0.04 | 0.11 | 2.67–2.78 | 5% |
| bfs-int | Marimay VM (source run) | 0.16 | 0.38 | 68.73–69.11 | 2% |
| bfs-record | Marimay native | 0.00 | 0.01 | 2.66–2.66 | 2% |
| bfs-record | Go native | 0.04 | 0.10 | 2.93–3.03 | 4% |
| bfs-record | Rust native | 0.05 | 0.13 | 2.43–2.56 | 5% |
| bfs-record | Marimay VM (source run) | 0.07 | 0.15 | 69.03–69.17 | 2% |
| catalog-pipeline | Marimay native | 0.01 | 0.14 | 2.39–2.53 | 6% |
| catalog-pipeline | Go native | 0.05 | 0.15 | 2.83–2.98 | 5% |
| catalog-pipeline | Rust native | 0.07 | 0.15 | 2.48–2.63 | 8% |
| catalog-pipeline | Marimay VM (source run) | 0.07 | 0.20 | 69.15–69.34 | 2% |
| parse-result | Marimay native | 0.00 | 0.03 | 2.60–2.63 | 2% |
| parse-result | Go native | 0.06 | 0.16 | 2.88–3.04 | 6% |
| parse-result | Rust native | 0.01 | 0.04 | 2.43–2.47 | 2% |
| parse-result | Marimay VM (source run) | 0.06 | 0.33 | 68.53–68.86 | 2% |

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

Command: `benchmarks/catalog_bench.py --profile smoke --engine both --verify-only --output benchmarks/results/catalog-installed-scalar-arrays-2026-09-09.md`
