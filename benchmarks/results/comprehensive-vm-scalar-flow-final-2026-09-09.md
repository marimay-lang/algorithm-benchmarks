# Catalogue and language benchmark

Generated: 2026-09-09T15:24:05+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay VM (source run) ms |
|---|---|---|
| title-search-10k | 10,000 × 128 | 157.57 |
| title-search-100k | 100,000 × 128 | 938.41 |
| normalize-title | 10,000 × 1 | 232.48 |
| word-frequency | 10,000 × 10 | 411.72 |
| report-builder | 10,000 × 1 | 202.05 |
| report-concat | 10,000 × 1 | 278.67 |
| map-int | 4,096 × 32 | 114.05 |
| map-string | 4,096 × 32 | 143.21 |
| map-string-book | 10,000 × 4 | 159.83 |
| set-string-churn | 4,096 × 8 | 164.00 |
| catalog-match | 10,000 × 32 | 368.41 |
| catalog-dotcall | 10,000 × 32 | 294.34 |
| catalog-interface | 10,000 × 32 | 405.71 |
| record-reference-copy | 1,024 × 128 | 214.21 |
| record-create | 1,024 × 128 | 249.99 |
| array-grow | 100,000 × 4 | 226.08 |
| array-reserved | 100,000 × 4 | 225.55 |
| bfs-int | 4,096 × 16 | 232.50 |
| bfs-record | 4,096 × 16 | 250.31 |
| catalog-pipeline | 10,000 × 16 | 583.21 |
| parse-result | 10,000 × 8 | 142.42 |
| insertion | fixed anchor | 5946.71 |
| heap-sort | fixed anchor | 1684.71 |
| stack | fixed anchor | 1126.89 |
| queue | fixed anchor | 1241.04 |
| min-heap | fixed anchor | 5856.56 |
| dsu | fixed anchor | 5658.36 |
| bfs | fixed anchor | 5565.16 |
| dijkstra | fixed anchor | 6755.03 |
| frequency-map | fixed anchor | 485.68 |
| unique-set | fixed anchor | 363.81 |
| rune-frequency | fixed anchor | 274.80 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay VM (source run) | 1.60 | 4.14 | 155.02–159.16 | 3% |
| title-search-100k | Marimay VM (source run) | 9.36 | 31.73 | 929.05–960.78 | 3% |
| normalize-title | Marimay VM (source run) | 1.09 | 4.16 | 231.39–235.56 | 2% |
| word-frequency | Marimay VM (source run) | 0.61 | 7.21 | 411.10–418.31 | 2% |
| report-builder | Marimay VM (source run) | 0.74 | 5.38 | 201.31–206.70 | 3% |
| report-concat | Marimay VM (source run) | 0.75 | 2.91 | 277.93–280.83 | 2% |
| map-int | Marimay VM (source run) | 0.35 | 0.86 | 113.70–114.56 | 2% |
| map-string | Marimay VM (source run) | 0.37 | 2.12 | 142.85–144.96 | 2% |
| map-string-book | Marimay VM (source run) | 0.61 | 1.38 | 159.07–160.44 | 2% |
| set-string-churn | Marimay VM (source run) | 0.39 | 1.59 | 162.80–164.39 | 2% |
| catalog-match | Marimay VM (source run) | 1.30 | 5.00 | 367.11–372.11 | 2% |
| catalog-dotcall | Marimay VM (source run) | 1.22 | 3.29 | 292.27–295.56 | 2% |
| catalog-interface | Marimay VM (source run) | 0.39 | 1.63 | 405.32–406.95 | 2% |
| record-reference-copy | Marimay VM (source run) | 0.42 | 1.16 | 213.47–214.63 | 2% |
| record-create | Marimay VM (source run) | 0.25 | 3.03 | 249.74–252.78 | 2% |
| array-grow | Marimay VM (source run) | 3.19 | 99.88 | 222.88–322.76 | 44% |
| array-reserved | Marimay VM (source run) | 0.55 | 2.42 | 223.68–226.10 | 2% |
| bfs-int | Marimay VM (source run) | 0.31 | 0.83 | 232.19–233.02 | 2% |
| bfs-record | Marimay VM (source run) | 0.43 | 0.92 | 249.88–250.80 | 2% |
| catalog-pipeline | Marimay VM (source run) | 4.73 | 86.95 | 578.47–665.42 | 15% |
| parse-result | Marimay VM (source run) | 0.49 | 6.01 | 141.94–147.95 | 4% |
| insertion | Marimay VM (source run) | 8.45 | 21.18 | 5938.26–5959.43 | 2% |
| heap-sort | Marimay VM (source run) | 1.29 | 4.18 | 1683.42–1687.60 | 2% |
| stack | Marimay VM (source run) | 2.82 | 17.87 | 1124.08–1141.95 | 2% |
| queue | Marimay VM (source run) | 2.55 | 8.64 | 1238.49–1247.13 | 2% |
| min-heap | Marimay VM (source run) | 1.18 | 78.53 | 5779.20–5857.73 | 2% |
| dsu | Marimay VM (source run) | 98.58 | 217.52 | 5559.77–5777.30 | 5% |
| bfs | Marimay VM (source run) | 7.28 | 21.75 | 5550.69–5572.44 | 2% |
| dijkstra | Marimay VM (source run) | 11.25 | 163.66 | 6743.78–6907.44 | 2% |
| frequency-map | Marimay VM (source run) | 3.41 | 94.15 | 482.27–576.42 | 19% |
| unique-set | Marimay VM (source run) | 0.81 | 10.06 | 354.55–364.61 | 3% |
| rune-frequency | Marimay VM (source run) | 0.15 | 1.30 | 274.65–275.96 | 2% |

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

Command: `./benchmarks/catalog_bench.py --anchors --engine vm --samples 3 --warmups 0 --verify-only --output benchmarks/results/comprehensive-vm-scalar-flow-final-2026-09-09.md`
