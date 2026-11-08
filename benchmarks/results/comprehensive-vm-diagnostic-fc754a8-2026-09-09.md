# Catalogue and language benchmark

Generated: 2026-09-09T12:15:01+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay VM (source run) ms |
|---|---|---|
| title-search-10k | 10,000 × 128 | 177.21 |
| title-search-100k | 100,000 × 128 | 1047.28 |
| normalize-title | 10,000 × 1 | 280.65 |
| word-frequency | 10,000 × 10 | 480.39 |
| report-builder | 10,000 × 1 | 222.49 |
| report-concat | 10,000 × 1 | 293.90 |
| map-int | 4,096 × 32 | 133.71 |
| map-string | 4,096 × 32 | 160.53 |
| map-string-book | 10,000 × 4 | 171.96 |
| set-string-churn | 4,096 × 8 | 182.16 |
| catalog-match | 10,000 × 32 | 417.63 |
| catalog-dotcall | 10,000 × 32 | 348.38 |
| catalog-interface | 10,000 × 32 | 434.62 |
| record-reference-copy | 1,024 × 128 | 267.85 |
| record-create | 1,024 × 128 | 304.60 |
| array-grow | 100,000 × 4 | 359.02 |
| array-reserved | 100,000 × 4 | 358.78 |
| bfs-int | 4,096 × 16 | 522.18 |
| bfs-record | 4,096 × 16 | 531.18 |
| catalog-pipeline | 10,000 × 16 | 760.54 |
| parse-result | 10,000 × 8 | 154.17 |
| insertion | fixed anchor | 21202.58 |
| heap-sort | fixed anchor | 5989.24 |
| stack | fixed anchor | 1336.43 |
| queue | fixed anchor | 1463.45 |
| min-heap | fixed anchor | 9232.36 |
| dsu | fixed anchor | 12278.35 |
| bfs | fixed anchor | 12940.75 |
| dijkstra | fixed anchor | 10480.94 |
| frequency-map | fixed anchor | 640.47 |
| unique-set | fixed anchor | 521.64 |
| rune-frequency | fixed anchor | 346.26 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay VM (source run) | 0.94 | 6.87 | 176.27–183.14 | 4% |
| title-search-100k | Marimay VM (source run) | 3.99 | 11.69 | 1039.58–1051.27 | 2% |
| normalize-title | Marimay VM (source run) | 0.86 | 1.83 | 279.68–281.50 | 2% |
| word-frequency | Marimay VM (source run) | 1.04 | 3.48 | 477.94–481.42 | 2% |
| report-builder | Marimay VM (source run) | 0.25 | 0.77 | 221.97–222.74 | 2% |
| report-concat | Marimay VM (source run) | 0.66 | 1.65 | 292.92–294.57 | 2% |
| map-int | Marimay VM (source run) | 0.12 | 1.42 | 132.42–133.83 | 2% |
| map-string | Marimay VM (source run) | 0.39 | 2.13 | 160.14–162.27 | 2% |
| map-string-book | Marimay VM (source run) | 0.03 | 3.05 | 171.94–174.99 | 2% |
| set-string-churn | Marimay VM (source run) | 0.08 | 1.48 | 182.08–183.56 | 2% |
| catalog-match | Marimay VM (source run) | 0.25 | 4.10 | 417.38–421.48 | 2% |
| catalog-dotcall | Marimay VM (source run) | 3.54 | 8.05 | 343.86–351.91 | 3% |
| catalog-interface | Marimay VM (source run) | 0.49 | 5.00 | 430.11–435.11 | 2% |
| record-reference-copy | Marimay VM (source run) | 1.19 | 2.57 | 266.65–269.22 | 2% |
| record-create | Marimay VM (source run) | 1.49 | 3.15 | 303.11–306.26 | 2% |
| array-grow | Marimay VM (source run) | 1.69 | 4.01 | 356.70–360.71 | 2% |
| array-reserved | Marimay VM (source run) | 0.52 | 1.82 | 357.48–359.30 | 2% |
| bfs-int | Marimay VM (source run) | 1.93 | 5.09 | 519.02–524.11 | 2% |
| bfs-record | Marimay VM (source run) | 0.97 | 3.90 | 530.21–534.11 | 2% |
| catalog-pipeline | Marimay VM (source run) | 0.64 | 1.41 | 759.90–761.31 | 2% |
| parse-result | Marimay VM (source run) | 0.80 | 2.65 | 153.37–156.02 | 2% |
| insertion | Marimay VM (source run) | 125.84 | 357.95 | 20970.47–21328.42 | 2% |
| heap-sort | Marimay VM (source run) | 2.90 | 12.73 | 5979.41–5992.14 | 2% |
| stack | Marimay VM (source run) | 8.21 | 25.14 | 1328.23–1353.37 | 2% |
| queue | Marimay VM (source run) | 2.72 | 7.32 | 1458.85–1466.16 | 2% |
| min-heap | Marimay VM (source run) | 8.68 | 35.66 | 9205.38–9241.04 | 2% |
| dsu | Marimay VM (source run) | 95.42 | 205.96 | 12182.92–12388.88 | 2% |
| bfs | Marimay VM (source run) | 24.32 | 178.00 | 12787.07–12965.07 | 2% |
| dijkstra | Marimay VM (source run) | 7.71 | 239.13 | 10473.24–10712.37 | 2% |
| frequency-map | Marimay VM (source run) | 6.48 | 13.14 | 633.81–646.96 | 3% |
| unique-set | Marimay VM (source run) | 0.02 | 4.05 | 521.62–525.67 | 2% |
| rune-frequency | Marimay VM (source run) | 4.04 | 8.68 | 342.21–350.89 | 4% |

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
- **insertion**: 50 × 2,500 generated integers
- **heap-sort**: 5 × 100,000 generated integers
- **stack**: 1,000,000 push + pop
- **queue**: 1,000,000 enqueue + dequeue
- **min-heap**: 500,000 insert + remove-min
- **dsu**: 100,000 nodes; 5,000,000 unions
- **bfs**: 300 × 20,000 nodes, degree 4
- **dijkstra**: 80 × 800 nodes, O(V²)
- **frequency-map**: 1,000,000 integers; 4,096-key histogram
- **unique-set**: 1,000,000 integers; distinct-value count
- **rune-frequency**: 450,000 Unicode scalars; 12-key histogram

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

Command: `./benchmarks/catalog_bench.py --anchors --engine vm --verify-only --samples 3 --warmups 0 --output benchmarks/results/comprehensive-vm-diagnostic-fc754a8-2026-09-09.md`
