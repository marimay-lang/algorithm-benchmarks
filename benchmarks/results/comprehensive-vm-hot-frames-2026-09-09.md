# Catalogue and language benchmark

Generated: 2026-09-09T14:08:21+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay VM (source run) ms |
|---|---|---|
| title-search-10k | 10,000 × 128 | 176.51 |
| title-search-100k | 100,000 × 128 | 1011.99 |
| normalize-title | 10,000 × 1 | 245.82 |
| word-frequency | 10,000 × 10 | 432.16 |
| report-builder | 10,000 × 1 | 214.90 |
| report-concat | 10,000 × 1 | 291.83 |
| map-int | 4,096 × 32 | 128.77 |
| map-string | 4,096 × 32 | 156.91 |
| map-string-book | 10,000 × 4 | 169.14 |
| set-string-churn | 4,096 × 8 | 175.73 |
| catalog-match | 10,000 × 32 | 385.08 |
| catalog-dotcall | 10,000 × 32 | 312.10 |
| catalog-interface | 10,000 × 32 | 422.84 |
| record-reference-copy | 1,024 × 128 | 227.06 |
| record-create | 1,024 × 128 | 261.71 |
| array-grow | 100,000 × 4 | 241.01 |
| array-reserved | 100,000 × 4 | 242.54 |
| bfs-int | 4,096 × 16 | 259.20 |
| bfs-record | 4,096 × 16 | 276.66 |
| catalog-pipeline | 10,000 × 16 | 611.76 |
| parse-result | 10,000 × 8 | 152.87 |
| insertion | fixed anchor | 7785.90 |
| heap-sort | fixed anchor | 1907.84 |
| stack | fixed anchor | 1148.75 |
| queue | fixed anchor | 1245.97 |
| min-heap | fixed anchor | 6108.61 |
| dsu | fixed anchor | 5879.89 |
| bfs | fixed anchor | 6269.73 |
| dijkstra | fixed anchor | 9322.01 |
| frequency-map | fixed anchor | 502.67 |
| unique-set | fixed anchor | 380.78 |
| rune-frequency | fixed anchor | 283.47 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay VM (source run) | 1.67 | 3.80 | 174.85–178.65 | 3% |
| title-search-100k | Marimay VM (source run) | 2.12 | 26.14 | 987.98–1014.11 | 3% |
| normalize-title | Marimay VM (source run) | 1.54 | 7.54 | 239.82–247.36 | 3% |
| word-frequency | Marimay VM (source run) | 1.71 | 13.46 | 420.41–433.87 | 3% |
| report-builder | Marimay VM (source run) | 0.14 | 1.64 | 213.39–215.03 | 2% |
| report-concat | Marimay VM (source run) | 1.44 | 9.55 | 283.72–293.27 | 3% |
| map-int | Marimay VM (source run) | 0.37 | 1.83 | 127.31–129.13 | 2% |
| map-string | Marimay VM (source run) | 0.86 | 2.56 | 156.04–158.60 | 2% |
| map-string-book | Marimay VM (source run) | 2.56 | 92.23 | 166.58–258.81 | 55% |
| set-string-churn | Marimay VM (source run) | 0.30 | 2.47 | 173.56–176.03 | 2% |
| catalog-match | Marimay VM (source run) | 3.09 | 7.25 | 380.92–388.17 | 2% |
| catalog-dotcall | Marimay VM (source run) | 2.20 | 8.11 | 306.19–314.30 | 3% |
| catalog-interface | Marimay VM (source run) | 2.65 | 7.17 | 418.32–425.49 | 2% |
| record-reference-copy | Marimay VM (source run) | 0.85 | 3.50 | 224.41–227.91 | 2% |
| record-create | Marimay VM (source run) | 2.42 | 98.80 | 259.29–358.09 | 38% |
| array-grow | Marimay VM (source run) | 1.53 | 5.15 | 237.39–242.54 | 2% |
| array-reserved | Marimay VM (source run) | 0.55 | 2.98 | 240.11–243.09 | 2% |
| bfs-int | Marimay VM (source run) | 1.83 | 4.13 | 256.90–261.03 | 2% |
| bfs-record | Marimay VM (source run) | 1.42 | 3.70 | 274.38–278.07 | 2% |
| catalog-pipeline | Marimay VM (source run) | 0.54 | 9.30 | 603.01–612.31 | 2% |
| parse-result | Marimay VM (source run) | 0.72 | 1.68 | 151.91–153.59 | 2% |
| insertion | Marimay VM (source run) | 13.62 | 34.66 | 7772.29–7806.94 | 2% |
| heap-sort | Marimay VM (source run) | 2.79 | 6.19 | 1904.44–1910.63 | 2% |
| stack | Marimay VM (source run) | 9.76 | 27.55 | 1138.99–1166.54 | 3% |
| queue | Marimay VM (source run) | 0.22 | 2.63 | 1245.75–1248.39 | 2% |
| min-heap | Marimay VM (source run) | 2.50 | 89.46 | 6106.11–6195.57 | 2% |
| dsu | Marimay VM (source run) | 25.88 | 67.17 | 5838.59–5905.76 | 2% |
| bfs | Marimay VM (source run) | 1.11 | 115.77 | 6268.61–6384.38 | 2% |
| dijkstra | Marimay VM (source run) | 13.71 | 191.24 | 9308.31–9499.55 | 2% |
| frequency-map | Marimay VM (source run) | 0.71 | 3.11 | 501.96–505.07 | 2% |
| unique-set | Marimay VM (source run) | 0.75 | 1.69 | 379.84–381.53 | 2% |
| rune-frequency | Marimay VM (source run) | 0.07 | 0.18 | 283.37–283.54 | 2% |

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

Command: `./benchmarks/catalog_bench.py --anchors --engine vm --verify-only --samples 3 --warmups 0 --output benchmarks/results/comprehensive-vm-hot-frames-2026-09-09.md`
