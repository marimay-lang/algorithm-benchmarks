# Catalogue and language benchmark

Generated: 2026-09-09T16:35:09+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay VM (source run) ms |
|---|---|---|
| title-search-10k | 10,000 × 128 | 139.43 |
| title-search-100k | 100,000 × 128 | 741.52 |
| normalize-title | 10,000 × 1 | 226.32 |
| word-frequency | 10,000 × 10 | 400.43 |
| report-builder | 10,000 × 1 | 196.50 |
| report-concat | 10,000 × 1 | 277.08 |
| map-int | 4,096 × 32 | 114.67 |
| map-string | 4,096 × 32 | 140.43 |
| map-string-book | 10,000 × 4 | 156.86 |
| set-string-churn | 4,096 × 8 | 159.69 |
| catalog-match | 10,000 × 32 | 352.96 |
| catalog-dotcall | 10,000 × 32 | 287.49 |
| catalog-interface | 10,000 × 32 | 390.63 |
| record-reference-copy | 1,024 × 128 | 188.36 |
| record-create | 1,024 × 128 | 223.73 |
| array-grow | 100,000 × 4 | 230.37 |
| array-reserved | 100,000 × 4 | 229.87 |
| bfs-int | 4,096 × 16 | 246.70 |
| bfs-record | 4,096 × 16 | 252.27 |
| catalog-pipeline | 10,000 × 16 | 487.04 |
| parse-result | 10,000 × 8 | 141.18 |
| insertion | fixed anchor | 6383.49 |
| heap-sort | fixed anchor | 1915.86 |
| stack | fixed anchor | 1098.07 |
| queue | fixed anchor | 1182.45 |
| min-heap | fixed anchor | 3661.28 |
| dsu | fixed anchor | 4321.36 |
| bfs | fixed anchor | 5825.32 |
| dijkstra | fixed anchor | 2789.37 |
| frequency-map | fixed anchor | 497.18 |
| unique-set | fixed anchor | 358.36 |
| rune-frequency | fixed anchor | 265.70 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay VM (source run) | 0.34 | 0.85 | 138.92–139.77 | 2% |
| title-search-100k | Marimay VM (source run) | 0.09 | 1.34 | 740.26–741.60 | 2% |
| normalize-title | Marimay VM (source run) | 2.08 | 4.67 | 224.25–228.92 | 3% |
| word-frequency | Marimay VM (source run) | 2.96 | 6.33 | 397.06–403.39 | 2% |
| report-builder | Marimay VM (source run) | 2.09 | 4.33 | 194.41–198.74 | 3% |
| report-concat | Marimay VM (source run) | 2.01 | 6.10 | 272.99–279.09 | 2% |
| map-int | Marimay VM (source run) | 0.40 | 1.65 | 113.42–115.07 | 2% |
| map-string | Marimay VM (source run) | 2.25 | 7.58 | 138.18–145.76 | 5% |
| map-string-book | Marimay VM (source run) | 0.73 | 92.05 | 156.13–248.18 | 59% |
| set-string-churn | Marimay VM (source run) | 1.35 | 4.20 | 158.34–162.55 | 3% |
| catalog-match | Marimay VM (source run) | 2.16 | 6.59 | 350.80–357.38 | 2% |
| catalog-dotcall | Marimay VM (source run) | 0.77 | 3.70 | 284.57–288.27 | 2% |
| catalog-interface | Marimay VM (source run) | 1.97 | 6.93 | 388.67–395.59 | 2% |
| record-reference-copy | Marimay VM (source run) | 0.06 | 1.95 | 188.31–190.25 | 2% |
| record-create | Marimay VM (source run) | 1.05 | 2.38 | 222.39–224.77 | 2% |
| array-grow | Marimay VM (source run) | 0.71 | 1.50 | 229.58–231.08 | 2% |
| array-reserved | Marimay VM (source run) | 0.30 | 1.61 | 228.56–230.17 | 2% |
| bfs-int | Marimay VM (source run) | 1.21 | 2.85 | 245.06–247.92 | 2% |
| bfs-record | Marimay VM (source run) | 0.46 | 1.71 | 251.02–252.73 | 2% |
| catalog-pipeline | Marimay VM (source run) | 0.92 | 2.70 | 486.12–488.82 | 2% |
| parse-result | Marimay VM (source run) | 0.40 | 1.70 | 139.88–141.59 | 2% |
| insertion | Marimay VM (source run) | 11.48 | 35.21 | 6372.01–6407.22 | 2% |
| heap-sort | Marimay VM (source run) | 2.16 | 4.90 | 1913.11–1918.01 | 2% |
| stack | Marimay VM (source run) | 2.09 | 10.97 | 1095.98–1106.96 | 2% |
| queue | Marimay VM (source run) | 15.43 | 37.54 | 1160.35–1197.89 | 4% |
| min-heap | Marimay VM (source run) | 1.29 | 6.09 | 3660.00–3666.08 | 2% |
| dsu | Marimay VM (source run) | 40.19 | 111.60 | 4281.17–4392.76 | 3% |
| bfs | Marimay VM (source run) | 11.87 | 107.26 | 5813.46–5920.72 | 2% |
| dijkstra | Marimay VM (source run) | 6.47 | 97.04 | 2782.90–2879.93 | 3% |
| frequency-map | Marimay VM (source run) | 0.16 | 5.26 | 497.02–502.28 | 2% |
| unique-set | Marimay VM (source run) | 0.11 | 2.72 | 358.26–360.98 | 2% |
| rune-frequency | Marimay VM (source run) | 0.76 | 3.31 | 264.94–268.25 | 2% |

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
- Bun uses JavaScript numbers for bounded exact integers, UTF-16 strings with UTF-8 byte checksums, Map/Set and reference objects; storage and copying are runtime-controlled.
- Bun report-builder uses an array of chunks plus join; concatenation may use ropes. Split and scalar strings are independently retainable values, without a forced physical copy in JavaScript.
- TypeScript interfaces are erased; catalog-interface measures a materialized structural-interface array and an ordinary method call, not a guaranteed vtable dispatch.
- JavaScript has no reserve-only Array API: array-reserved uses new Array(n) plus indexed writes; array-grow uses push. These are equivalent values, not identical allocation/append traces.
- The per-workload Go targets are exploratory thresholds, not reviewed release budgets. No average score or general ‘Go parity’ verdict is computed.
- Short cases can be dominated by process startup and validation; repeat with larger documented inputs before attributing a difference to dispatch, GC or a particular primitive.
- Interface results include array construction/boxing and compiler devirtualization opportunities; they are not isolated virtual-call latency.

## Toolchains

- python: `3.9.6`
- marimay: `Marimay compiler 0.1.0-alpha.1`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Command: `./benchmarks/catalog_bench.py --engine vm --anchors --verify-only --output benchmarks/results/comprehensive-vm-reference-regions-2026-09-09.md`
