# Catalogue and language benchmark

Generated: 2026-09-09T15:11:10+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay VM (source run) ms |
|---|---|---|
| title-search-10k | 10,000 × 128 | 155.59 |
| title-search-100k | 100,000 × 128 | 923.23 |
| normalize-title | 10,000 × 1 | 233.17 |
| word-frequency | 10,000 × 10 | 412.74 |
| report-builder | 10,000 × 1 | 200.25 |
| report-concat | 10,000 × 1 | 275.12 |
| map-int | 4,096 × 32 | 113.93 |
| map-string | 4,096 × 32 | 143.05 |
| map-string-book | 10,000 × 4 | 159.32 |
| set-string-churn | 4,096 × 8 | 165.23 |
| catalog-match | 10,000 × 32 | 373.70 |
| catalog-dotcall | 10,000 × 32 | 297.08 |
| catalog-interface | 10,000 × 32 | 411.42 |
| record-reference-copy | 1,024 × 128 | 213.66 |
| record-create | 1,024 × 128 | 249.60 |
| array-grow | 100,000 × 4 | 225.82 |
| array-reserved | 100,000 × 4 | 225.28 |
| bfs-int | 4,096 × 16 | 231.69 |
| bfs-record | 4,096 × 16 | 249.64 |
| catalog-pipeline | 10,000 × 16 | 574.99 |
| parse-result | 10,000 × 8 | 139.70 |
| insertion | fixed anchor | 6107.29 |
| heap-sort | fixed anchor | 1688.42 |
| stack | fixed anchor | 1105.52 |
| queue | fixed anchor | 1212.54 |
| min-heap | fixed anchor | 5796.40 |
| dsu | fixed anchor | 5557.17 |
| bfs | fixed anchor | 5575.72 |
| dijkstra | fixed anchor | 6753.48 |
| frequency-map | fixed anchor | 482.00 |
| unique-set | fixed anchor | 360.45 |
| rune-frequency | fixed anchor | 276.65 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay VM (source run) | 0.15 | 2.10 | 155.44–157.55 | 2% |
| title-search-100k | Marimay VM (source run) | 10.14 | 24.25 | 909.12–933.37 | 3% |
| normalize-title | Marimay VM (source run) | 1.49 | 3.99 | 231.68–235.67 | 2% |
| word-frequency | Marimay VM (source run) | 0.39 | 0.83 | 412.31–413.14 | 2% |
| report-builder | Marimay VM (source run) | 0.58 | 1.23 | 199.67–200.90 | 2% |
| report-concat | Marimay VM (source run) | 0.96 | 5.89 | 274.15–280.04 | 2% |
| map-int | Marimay VM (source run) | 0.44 | 4.66 | 113.49–118.15 | 4% |
| map-string | Marimay VM (source run) | 0.78 | 4.41 | 142.26–146.68 | 3% |
| map-string-book | Marimay VM (source run) | 0.95 | 2.40 | 157.87–160.27 | 2% |
| set-string-churn | Marimay VM (source run) | 1.51 | 3.69 | 163.06–166.74 | 3% |
| catalog-match | Marimay VM (source run) | 1.81 | 11.86 | 363.65–375.51 | 3% |
| catalog-dotcall | Marimay VM (source run) | 1.43 | 6.02 | 292.49–298.51 | 2% |
| catalog-interface | Marimay VM (source run) | 0.06 | 0.98 | 410.50–411.48 | 2% |
| record-reference-copy | Marimay VM (source run) | 0.69 | 2.85 | 212.97–215.82 | 2% |
| record-create | Marimay VM (source run) | 0.04 | 2.70 | 246.94–249.64 | 2% |
| array-grow | Marimay VM (source run) | 2.40 | 4.83 | 223.39–228.22 | 3% |
| array-reserved | Marimay VM (source run) | 1.30 | 3.00 | 223.98–226.98 | 2% |
| bfs-int | Marimay VM (source run) | 0.31 | 1.68 | 231.38–233.07 | 2% |
| bfs-record | Marimay VM (source run) | 0.64 | 3.54 | 249.01–252.55 | 2% |
| catalog-pipeline | Marimay VM (source run) | 2.26 | 4.87 | 572.38–577.25 | 2% |
| parse-result | Marimay VM (source run) | 0.20 | 1.95 | 139.50–141.45 | 2% |
| insertion | Marimay VM (source run) | 20.05 | 109.51 | 6017.83–6127.34 | 2% |
| heap-sort | Marimay VM (source run) | 1.84 | 7.02 | 1683.24–1690.26 | 2% |
| stack | Marimay VM (source run) | 1.52 | 7.45 | 1099.60–1107.04 | 2% |
| queue | Marimay VM (source run) | 4.03 | 35.48 | 1208.51–1243.98 | 3% |
| min-heap | Marimay VM (source run) | 49.51 | 171.81 | 5746.89–5918.69 | 3% |
| dsu | Marimay VM (source run) | 5.33 | 84.13 | 5551.84–5635.98 | 2% |
| bfs | Marimay VM (source run) | 0.67 | 4.73 | 5571.66–5576.40 | 2% |
| dijkstra | Marimay VM (source run) | 2.55 | 19.59 | 6750.93–6770.53 | 2% |
| frequency-map | Marimay VM (source run) | 1.90 | 7.48 | 480.09–487.58 | 2% |
| unique-set | Marimay VM (source run) | 2.74 | 7.95 | 355.24–363.19 | 2% |
| rune-frequency | Marimay VM (source run) | 1.25 | 2.83 | 275.07–277.90 | 2% |

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

Command: `./benchmarks/catalog_bench.py --anchors --engine vm --samples 3 --warmups 0 --verify-only --output benchmarks/results/comprehensive-vm-scalar-flow-2026-09-09.md`
