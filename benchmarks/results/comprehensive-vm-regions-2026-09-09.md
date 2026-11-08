# Catalogue and language benchmark

Generated: 2026-09-09T14:18:01+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay VM (source run) ms |
|---|---|---|
| title-search-10k | 10,000 × 128 | 176.68 |
| title-search-100k | 100,000 × 128 | 1026.37 |
| normalize-title | 10,000 × 1 | 245.85 |
| word-frequency | 10,000 × 10 | 431.49 |
| report-builder | 10,000 × 1 | 215.46 |
| report-concat | 10,000 × 1 | 291.37 |
| map-int | 4,096 × 32 | 129.59 |
| map-string | 4,096 × 32 | 157.38 |
| map-string-book | 10,000 × 4 | 171.22 |
| set-string-churn | 4,096 × 8 | 177.04 |
| catalog-match | 10,000 × 32 | 389.59 |
| catalog-dotcall | 10,000 × 32 | 317.26 |
| catalog-interface | 10,000 × 32 | 423.50 |
| record-reference-copy | 1,024 × 128 | 228.18 |
| record-create | 1,024 × 128 | 265.38 |
| array-grow | 100,000 × 4 | 241.33 |
| array-reserved | 100,000 × 4 | 240.96 |
| bfs-int | 4,096 × 16 | 260.88 |
| bfs-record | 4,096 × 16 | 278.02 |
| catalog-pipeline | 10,000 × 16 | 611.02 |
| parse-result | 10,000 × 8 | 154.98 |
| insertion | fixed anchor | 7765.96 |
| heap-sort | fixed anchor | 1909.57 |
| stack | fixed anchor | 1140.22 |
| queue | fixed anchor | 1253.81 |
| min-heap | fixed anchor | 6086.82 |
| dsu | fixed anchor | 5780.01 |
| bfs | fixed anchor | 6256.77 |
| dijkstra | fixed anchor | 9409.11 |
| frequency-map | fixed anchor | 502.29 |
| unique-set | fixed anchor | 380.53 |
| rune-frequency | fixed anchor | 295.03 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay VM (source run) | 0.51 | 91.44 | 176.17–267.62 | 52% |
| title-search-100k | Marimay VM (source run) | 4.23 | 10.09 | 1022.14–1032.23 | 2% |
| normalize-title | Marimay VM (source run) | 0.24 | 1.20 | 245.62–246.82 | 2% |
| word-frequency | Marimay VM (source run) | 0.11 | 4.83 | 426.77–431.60 | 2% |
| report-builder | Marimay VM (source run) | 0.38 | 3.65 | 212.20–215.84 | 2% |
| report-concat | Marimay VM (source run) | 0.84 | 2.52 | 289.69–292.21 | 2% |
| map-int | Marimay VM (source run) | 0.07 | 1.45 | 128.21–129.66 | 2% |
| map-string | Marimay VM (source run) | 0.06 | 2.35 | 157.32–159.67 | 2% |
| map-string-book | Marimay VM (source run) | 0.67 | 1.84 | 170.05–171.88 | 2% |
| set-string-churn | Marimay VM (source run) | 0.46 | 1.56 | 176.59–178.14 | 2% |
| catalog-match | Marimay VM (source run) | 1.05 | 15.26 | 388.54–403.80 | 4% |
| catalog-dotcall | Marimay VM (source run) | 4.12 | 84.41 | 313.14–397.56 | 27% |
| catalog-interface | Marimay VM (source run) | 0.13 | 3.89 | 423.37–427.26 | 2% |
| record-reference-copy | Marimay VM (source run) | 0.26 | 1.08 | 227.37–228.44 | 2% |
| record-create | Marimay VM (source run) | 1.01 | 2.61 | 264.37–266.98 | 2% |
| array-grow | Marimay VM (source run) | 0.53 | 3.10 | 240.80–243.90 | 2% |
| array-reserved | Marimay VM (source run) | 1.06 | 5.48 | 239.90–245.38 | 2% |
| bfs-int | Marimay VM (source run) | 0.45 | 1.10 | 260.23–261.33 | 2% |
| bfs-record | Marimay VM (source run) | 0.31 | 1.21 | 277.11–278.33 | 2% |
| catalog-pipeline | Marimay VM (source run) | 0.25 | 6.63 | 610.77–617.40 | 2% |
| parse-result | Marimay VM (source run) | 0.28 | 1.36 | 153.90–155.26 | 2% |
| insertion | Marimay VM (source run) | 3.80 | 22.22 | 7762.15–7784.37 | 2% |
| heap-sort | Marimay VM (source run) | 1.41 | 84.94 | 1908.16–1993.10 | 4% |
| stack | Marimay VM (source run) | 1.55 | 3.89 | 1137.89–1141.78 | 2% |
| queue | Marimay VM (source run) | 19.53 | 104.40 | 1234.28–1338.68 | 8% |
| min-heap | Marimay VM (source run) | 16.92 | 105.30 | 6069.90–6175.20 | 2% |
| dsu | Marimay VM (source run) | 6.12 | 26.19 | 5773.89–5800.08 | 2% |
| bfs | Marimay VM (source run) | 5.60 | 42.99 | 6251.16–6294.15 | 2% |
| dijkstra | Marimay VM (source run) | 55.57 | 175.16 | 9353.54–9528.70 | 2% |
| frequency-map | Marimay VM (source run) | 0.92 | 23.10 | 501.37–524.47 | 5% |
| unique-set | Marimay VM (source run) | 0.29 | 0.74 | 380.08–380.83 | 2% |
| rune-frequency | Marimay VM (source run) | 0.05 | 0.93 | 294.15–295.08 | 2% |

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

Command: `./benchmarks/catalog_bench.py --anchors --engine vm --verify-only --samples 3 --warmups 0 --output benchmarks/results/comprehensive-vm-regions-2026-09-09.md`
