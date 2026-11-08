# Catalogue and language benchmark

Generated: 2026-09-09T11:22:34+07:00; profile: **smoke**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | Marimay VM (source run) ms |
|---|---|---|---|---|---|
| title-search-10k | 32 × 3 | 2.86 | 3.18 | 3.00 | 81.45 |
| title-search-100k | 128 × 3 | 2.93 | 3.08 | 2.93 | 81.27 |
| normalize-title | 32 × 3 | 3.38 | 3.16 | 2.67 | 82.96 |
| word-frequency | 32 × 3 | 2.61 | 2.99 | 2.60 | 81.51 |
| report-builder | 32 × 3 | 2.90 | 3.13 | 2.54 | 82.35 |
| report-concat | 32 × 3 | 3.03 | 3.25 | 2.87 | 82.58 |
| map-int | 32 × 3 | 2.72 | 3.10 | 2.52 | 81.07 |
| map-string | 32 × 3 | 2.52 | 3.00 | 2.52 | 81.36 |
| map-string-book | 32 × 3 | 2.92 | 3.15 | 2.50 | 81.28 |
| set-string-churn | 32 × 3 | 3.00 | 3.08 | 2.87 | 81.38 |
| catalog-match | 32 × 3 | 2.92 | 3.12 | 2.53 | 81.44 |
| catalog-dotcall | 32 × 3 | 2.50 | 2.99 | 2.45 | 81.48 |
| catalog-interface | 32 × 3 | 2.78 | 3.04 | 2.60 | 81.42 |
| record-reference-copy | 32 × 3 | 2.81 | 3.11 | 2.91 | 81.55 |
| record-create | 32 × 3 | 2.84 | 3.05 | 2.57 | 81.38 |
| array-grow | 32 × 3 | 2.47 | 3.03 | 2.57 | 81.33 |
| array-reserved | 32 × 3 | 2.74 | 3.03 | 2.54 | 81.18 |
| bfs-int | 32 × 3 | 2.93 | 3.19 | 2.90 | 82.16 |
| bfs-record | 32 × 3 | 2.82 | 3.07 | 2.59 | 82.30 |
| catalog-pipeline | 32 × 3 | 2.52 | 3.03 | 2.53 | 82.07 |
| parse-result | 32 × 3 | 2.86 | 3.12 | 2.57 | 81.17 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.10 | 543.24 | 2.76–546.00 | 18963% |
| title-search-10k | Go native | 0.05 | 27.47 | 3.13–30.60 | 865% |
| title-search-10k | Rust native | 0.16 | 380.76 | 2.84–383.61 | 12683% |
| title-search-10k | Marimay VM (source run) | 0.44 | 30.06 | 81.01–111.06 | 37% |
| title-search-100k | Marimay native | 0.02 | 0.37 | 2.91–3.28 | 13% |
| title-search-100k | Go native | 0.03 | 0.08 | 3.03–3.11 | 3% |
| title-search-100k | Rust native | 0.15 | 0.58 | 2.50–3.08 | 20% |
| title-search-100k | Marimay VM (source run) | 0.07 | 0.41 | 81.19–81.60 | 2% |
| normalize-title | Marimay native | 0.01 | 0.11 | 3.37–3.48 | 3% |
| normalize-title | Go native | 0.06 | 0.19 | 3.04–3.22 | 6% |
| normalize-title | Rust native | 0.05 | 0.17 | 2.61–2.79 | 7% |
| normalize-title | Marimay VM (source run) | 0.02 | 0.35 | 82.93–83.28 | 2% |
| word-frequency | Marimay native | 0.01 | 0.11 | 2.60–2.71 | 4% |
| word-frequency | Go native | 0.00 | 0.06 | 2.93–2.99 | 2% |
| word-frequency | Rust native | 0.01 | 0.07 | 2.55–2.62 | 3% |
| word-frequency | Marimay VM (source run) | 0.01 | 0.32 | 81.49–81.82 | 2% |
| report-builder | Marimay native | 0.00 | 0.15 | 2.90–3.05 | 5% |
| report-builder | Go native | 0.06 | 0.13 | 3.06–3.19 | 6% |
| report-builder | Rust native | 0.03 | 0.07 | 2.50–2.57 | 3% |
| report-builder | Marimay VM (source run) | 0.08 | 0.22 | 82.27–82.48 | 2% |
| report-concat | Marimay native | 0.04 | 0.35 | 3.00–3.35 | 12% |
| report-concat | Go native | 0.05 | 0.27 | 3.02–3.29 | 8% |
| report-concat | Rust native | 0.01 | 0.11 | 2.86–2.98 | 4% |
| report-concat | Marimay VM (source run) | 0.19 | 0.45 | 82.39–82.84 | 2% |
| map-int | Marimay native | 0.02 | 0.69 | 2.70–3.39 | 25% |
| map-int | Go native | 0.01 | 0.08 | 3.09–3.17 | 3% |
| map-int | Rust native | 0.01 | 0.11 | 2.51–2.62 | 4% |
| map-int | Marimay VM (source run) | 0.12 | 1.48 | 80.94–82.42 | 2% |
| map-string | Marimay native | 0.01 | 0.81 | 2.51–3.33 | 32% |
| map-string | Go native | 0.00 | 0.08 | 2.93–3.00 | 3% |
| map-string | Rust native | 0.02 | 0.05 | 2.49–2.55 | 3% |
| map-string | Marimay VM (source run) | 0.02 | 0.15 | 81.22–81.38 | 2% |
| map-string-book | Marimay native | 0.05 | 0.11 | 2.86–2.97 | 5% |
| map-string-book | Go native | 0.00 | 0.10 | 3.05–3.15 | 3% |
| map-string-book | Rust native | 0.01 | 0.10 | 2.49–2.59 | 4% |
| map-string-book | Marimay VM (source run) | 0.02 | 0.24 | 81.26–81.49 | 2% |
| set-string-churn | Marimay native | 0.00 | 0.04 | 2.97–3.01 | 2% |
| set-string-churn | Go native | 0.01 | 0.03 | 3.05–3.08 | 2% |
| set-string-churn | Rust native | 0.02 | 0.08 | 2.85–2.93 | 3% |
| set-string-churn | Marimay VM (source run) | 0.01 | 0.15 | 81.36–81.51 | 2% |
| catalog-match | Marimay native | 0.01 | 0.16 | 2.92–3.07 | 5% |
| catalog-match | Go native | 0.01 | 0.07 | 3.11–3.18 | 2% |
| catalog-match | Rust native | 0.04 | 0.10 | 2.49–2.59 | 5% |
| catalog-match | Marimay VM (source run) | 0.26 | 0.59 | 81.11–81.71 | 2% |
| catalog-dotcall | Marimay native | 0.00 | 0.06 | 2.44–2.50 | 2% |
| catalog-dotcall | Go native | 0.03 | 0.09 | 2.93–3.02 | 3% |
| catalog-dotcall | Rust native | 0.01 | 0.03 | 2.43–2.46 | 2% |
| catalog-dotcall | Marimay VM (source run) | 0.17 | 11.34 | 81.31–92.65 | 14% |
| catalog-interface | Marimay native | 0.00 | 0.53 | 2.77–3.31 | 19% |
| catalog-interface | Go native | 0.03 | 0.28 | 3.01–3.29 | 9% |
| catalog-interface | Rust native | 0.02 | 0.07 | 2.58–2.66 | 3% |
| catalog-interface | Marimay VM (source run) | 0.14 | 0.35 | 81.28–81.63 | 2% |
| record-reference-copy | Marimay native | 0.04 | 0.11 | 2.77–2.88 | 5% |
| record-reference-copy | Go native | 0.02 | 0.05 | 3.08–3.14 | 2% |
| record-reference-copy | Rust native | 0.09 | 0.21 | 2.79–3.00 | 9% |
| record-reference-copy | Marimay VM (source run) | 0.01 | 0.28 | 81.28–81.55 | 2% |
| record-create | Marimay native | 0.06 | 0.12 | 2.79–2.90 | 6% |
| record-create | Go native | 0.09 | 0.22 | 2.96–3.18 | 8% |
| record-create | Rust native | 0.00 | 0.04 | 2.53–2.57 | 2% |
| record-create | Marimay VM (source run) | 0.05 | 0.64 | 81.33–81.98 | 2% |
| array-grow | Marimay native | 0.01 | 0.07 | 2.47–2.53 | 3% |
| array-grow | Go native | 0.01 | 0.08 | 3.02–3.10 | 3% |
| array-grow | Rust native | 0.02 | 0.15 | 2.44–2.59 | 6% |
| array-grow | Marimay VM (source run) | 0.04 | 0.09 | 81.28–81.37 | 2% |
| array-reserved | Marimay native | 0.02 | 0.07 | 2.69–2.76 | 3% |
| array-reserved | Go native | 0.04 | 0.12 | 2.96–3.08 | 4% |
| array-reserved | Rust native | 0.01 | 0.15 | 2.53–2.67 | 6% |
| array-reserved | Marimay VM (source run) | 0.05 | 1.98 | 81.13–83.10 | 2% |
| bfs-int | Marimay native | 0.18 | 0.45 | 2.75–3.20 | 19% |
| bfs-int | Go native | 0.07 | 0.25 | 3.01–3.26 | 8% |
| bfs-int | Rust native | 0.01 | 0.10 | 2.89–2.99 | 4% |
| bfs-int | Marimay VM (source run) | 0.12 | 0.88 | 82.04–82.92 | 2% |
| bfs-record | Marimay native | 0.05 | 0.13 | 2.74–2.87 | 5% |
| bfs-record | Go native | 0.01 | 0.15 | 3.05–3.20 | 5% |
| bfs-record | Rust native | 0.02 | 0.11 | 2.50–2.61 | 4% |
| bfs-record | Marimay VM (source run) | 0.01 | 0.21 | 82.10–82.31 | 2% |
| catalog-pipeline | Marimay native | 0.03 | 0.13 | 2.50–2.63 | 5% |
| catalog-pipeline | Go native | 0.02 | 0.10 | 2.96–3.05 | 3% |
| catalog-pipeline | Rust native | 0.05 | 0.21 | 2.49–2.69 | 8% |
| catalog-pipeline | Marimay VM (source run) | 0.23 | 0.86 | 81.44–82.30 | 2% |
| parse-result | Marimay native | 0.04 | 0.15 | 2.74–2.90 | 5% |
| parse-result | Go native | 0.06 | 0.18 | 3.06–3.25 | 6% |
| parse-result | Rust native | 0.05 | 0.12 | 2.51–2.62 | 6% |
| parse-result | Marimay VM (source run) | 0.12 | 0.62 | 80.67–81.30 | 2% |

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

Command: `./benchmarks/catalog_bench.py --profile smoke --verify-only --output benchmarks/results/catalog-vm-string-lifetime-smoke-2026-09-09.md`
