# Catalogue and language benchmark

Generated: 2026-09-09T15:53:24+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay VM (source run) ms |
|---|---|---|
| title-search-10k | 10,000 × 128 | 152.08 |
| title-search-100k | 100,000 × 128 | 909.77 |
| normalize-title | 10,000 × 1 | 227.19 |
| word-frequency | 10,000 × 10 | 405.18 |
| report-builder | 10,000 × 1 | 188.71 |
| report-concat | 10,000 × 1 | 264.88 |
| map-int | 4,096 × 32 | 111.43 |
| map-string | 4,096 × 32 | 139.89 |
| map-string-book | 10,000 × 4 | 154.26 |
| set-string-churn | 4,096 × 8 | 160.19 |
| catalog-match | 10,000 × 32 | 358.19 |
| catalog-dotcall | 10,000 × 32 | 287.97 |
| catalog-interface | 10,000 × 32 | 398.44 |
| record-reference-copy | 1,024 × 128 | 207.99 |
| record-create | 1,024 × 128 | 242.66 |
| array-grow | 100,000 × 4 | 221.54 |
| array-reserved | 100,000 × 4 | 221.72 |
| bfs-int | 4,096 × 16 | 227.27 |
| bfs-record | 4,096 × 16 | 244.21 |
| catalog-pipeline | 10,000 × 16 | 563.29 |
| parse-result | 10,000 × 8 | 137.14 |
| insertion | fixed anchor | 5899.92 |
| heap-sort | fixed anchor | 1662.72 |
| stack | fixed anchor | 1093.31 |
| queue | fixed anchor | 1188.10 |
| min-heap | fixed anchor | 5609.20 |
| dsu | fixed anchor | 5374.60 |
| bfs | fixed anchor | 5479.15 |
| dijkstra | fixed anchor | 2382.35 |
| frequency-map | fixed anchor | 472.15 |
| unique-set | fixed anchor | 346.62 |
| rune-frequency | fixed anchor | 248.15 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay VM (source run) | 1.07 | 2.66 | 150.50–153.15 | 2% |
| title-search-100k | Marimay VM (source run) | 20.54 | 48.82 | 889.22–938.04 | 7% |
| normalize-title | Marimay VM (source run) | 0.02 | 0.89 | 226.32–227.21 | 2% |
| word-frequency | Marimay VM (source run) | 0.06 | 1.08 | 404.16–405.24 | 2% |
| report-builder | Marimay VM (source run) | 0.55 | 2.58 | 188.16–190.74 | 2% |
| report-concat | Marimay VM (source run) | 0.33 | 2.81 | 262.40–265.21 | 2% |
| map-int | Marimay VM (source run) | 0.56 | 1.94 | 110.88–112.82 | 2% |
| map-string | Marimay VM (source run) | 0.37 | 1.00 | 139.52–140.53 | 2% |
| map-string-book | Marimay VM (source run) | 0.03 | 0.39 | 154.23–154.62 | 2% |
| set-string-churn | Marimay VM (source run) | 0.47 | 1.55 | 159.10–160.66 | 2% |
| catalog-match | Marimay VM (source run) | 0.29 | 2.66 | 357.91–360.57 | 2% |
| catalog-dotcall | Marimay VM (source run) | 1.13 | 3.22 | 286.84–290.06 | 2% |
| catalog-interface | Marimay VM (source run) | 0.21 | 0.43 | 398.22–398.65 | 2% |
| record-reference-copy | Marimay VM (source run) | 0.60 | 1.58 | 207.01–208.59 | 2% |
| record-create | Marimay VM (source run) | 1.60 | 4.10 | 241.05–245.16 | 2% |
| array-grow | Marimay VM (source run) | 1.20 | 3.88 | 218.85–222.73 | 2% |
| array-reserved | Marimay VM (source run) | 0.24 | 6.78 | 221.48–228.26 | 3% |
| bfs-int | Marimay VM (source run) | 0.89 | 4.89 | 226.38–231.27 | 2% |
| bfs-record | Marimay VM (source run) | 0.33 | 0.68 | 243.88–244.57 | 2% |
| catalog-pipeline | Marimay VM (source run) | 1.03 | 2.19 | 562.26–564.45 | 2% |
| parse-result | Marimay VM (source run) | 1.05 | 2.59 | 135.60–138.19 | 2% |
| insertion | Marimay VM (source run) | 0.49 | 6.29 | 5894.11–5900.41 | 2% |
| heap-sort | Marimay VM (source run) | 0.94 | 3.82 | 1661.77–1665.60 | 2% |
| stack | Marimay VM (source run) | 22.43 | 49.34 | 1070.88–1120.22 | 6% |
| queue | Marimay VM (source run) | 0.53 | 4.16 | 1184.47–1188.63 | 2% |
| min-heap | Marimay VM (source run) | 6.92 | 48.98 | 5602.29–5651.27 | 2% |
| dsu | Marimay VM (source run) | 0.56 | 16.14 | 5359.02–5375.16 | 2% |
| bfs | Marimay VM (source run) | 8.06 | 19.44 | 5471.09–5490.53 | 2% |
| dijkstra | Marimay VM (source run) | 1.05 | 5.42 | 2381.30–2386.72 | 2% |
| frequency-map | Marimay VM (source run) | 0.29 | 0.63 | 471.86–472.49 | 2% |
| unique-set | Marimay VM (source run) | 0.12 | 0.73 | 346.01–346.74 | 2% |
| rune-frequency | Marimay VM (source run) | 0.08 | 0.35 | 247.87–248.23 | 2% |

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

Command: `benchmarks/catalog_bench.py --anchors --engine vm --verify-only --samples 3 --warmups 0 --output benchmarks/results/comprehensive-vm-scalar-arrays-2026-09-09.md`
