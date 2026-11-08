# Catalogue and language benchmark

Generated: 2026-09-09T15:10:25+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **11** after **3** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | native / Go | native / Rust | Go target | Assessment |
|---|---|---|---|---|---|---|---|---|
| title-search-10k | 10,000 × 128 | 9.10 | 4.29 | 4.29 | 2.12× | 2.12× | — | measured |
| title-search-100k | 100,000 × 128 | 81.13 | 15.37 | 18.19 | 5.28× | 4.46× | — | measured |
| normalize-title | 10,000 × 1 | 57.43 | 8.95 | 11.03 | 6.42× | 5.21× | — | measured |
| word-frequency | 10,000 × 10 | 145.78 | 19.07 | 30.38 | 7.65× | 4.80× | ≤ 2.0× | above target |
| report-builder | 10,000 × 1 | 15.03 | 5.10 | 5.24 | 2.95× | 2.87× | — | measured |
| report-concat | 10,000 × 1 | 98.12 | 80.87 | 47.69 | 1.21× | 2.06× | — | measured |
| map-int | 4,096 × 32 | 7.65 | 5.10 | 5.84 | 1.50× | 1.31× | ≤ 1.5× | above target |
| map-string | 4,096 × 32 | 23.19 | 7.46 | 9.85 | 3.11× | 2.35× | ≤ 2.0× | above target |
| map-string-book | 10,000 × 4 | 31.60 | 6.59 | 10.52 | 4.79× | 3.00× | — | measured |
| set-string-churn | 4,096 × 8 | 47.43 | 9.94 | 17.06 | 4.77× | 2.78× | — | measured |
| catalog-match | 10,000 × 32 | 13.13 | 4.77 | 3.85 | 2.75× | 3.41× | ≤ 1.5× | above target |
| catalog-dotcall | 10,000 × 32 | 8.32 | 4.63 | 3.69 | 1.80× | 2.26× | — | measured |
| catalog-interface | 10,000 × 32 | 11.96 | 4.50 | 3.70 | 2.66× | 3.23× | — | measured |
| record-reference-copy | 1,024 × 128 | 6.75 | 4.40 | 3.20 | 1.53× | 2.11× | — | measured |
| record-create | 1,024 × 128 | 23.13 | 6.93 | 6.30 | 3.34× | 3.67× | — | measured |
| array-grow | 100,000 × 4 | 6.71 | 6.35 | 4.11 | 1.06× | 1.63× | — | measured |
| array-reserved | 100,000 × 4 | 6.58 | 5.19 | 4.16 | 1.27× | 1.58× | — | measured |
| bfs-int | 4,096 × 16 | 7.43 | 5.27 | 4.27 | 1.41× | 1.74× | — | measured |
| bfs-record | 4,096 × 16 | 9.21 | 5.68 | 4.58 | 1.62× | 2.01× | — | measured |
| catalog-pipeline | 10,000 × 16 | 37.69 | 7.76 | 9.99 | 4.85× | 3.77× | — | measured |
| parse-result | 10,000 × 8 | 19.19 | 5.87 | 5.83 | 3.27× | 3.29× | — | measured |
| insertion | fixed anchor | 49.86 | 29.20 | 28.47 | 1.71× | 1.75× | — | measured |
| heap-sort | fixed anchor | 32.42 | 39.27 | 22.16 | 0.83× | 1.46× | ≤ 1.3× | within target |
| stack | fixed anchor | 9.69 | 14.59 | 9.00 | 0.66× | 1.08× | ≤ 1.3× | within target |
| queue | fixed anchor | 9.83 | 14.65 | 8.99 | 0.67× | 1.09× | ≤ 1.3× | within target |
| min-heap | fixed anchor | 46.46 | 54.05 | 29.52 | 0.86× | 1.57× | ≤ 1.3× | within target |
| dsu | fixed anchor | 29.89 | 24.57 | 22.06 | 1.22× | 1.36× | — | measured |
| bfs | fixed anchor | 109.96 | 63.01 | 23.70 | 1.75× | 4.64× | — | measured |
| dijkstra | fixed anchor | 41.46 | 41.62 | 39.29 | 1.00× | 1.06× | ≤ 1.3× | within target |
| frequency-map | fixed anchor | 32.80 | 14.08 | 16.76 | 2.33× | 1.96× | — | noisy; repeat |
| unique-set | fixed anchor | 27.12 | 16.24 | 19.27 | 1.67× | 1.41× | — | measured |
| rune-frequency | fixed anchor | 22.52 | 5.92 | 6.02 | 3.80× | 3.74× | — | measured |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.16 | 0.28 | 8.91–9.51 | 5% |
| title-search-10k | Go native | 0.11 | 0.22 | 4.09–5.32 | 8% |
| title-search-10k | Rust native | 0.21 | 0.44 | 3.95–4.81 | 14% |
| title-search-100k | Marimay native | 1.37 | 3.04 | 78.71–83.45 | 5% |
| title-search-100k | Go native | 0.29 | 0.54 | 14.64–16.38 | 6% |
| title-search-100k | Rust native | 0.25 | 0.52 | 17.76–19.02 | 4% |
| normalize-title | Marimay native | 0.31 | 1.06 | 57.12–59.82 | 2% |
| normalize-title | Go native | 0.25 | 0.50 | 8.44–9.55 | 8% |
| normalize-title | Rust native | 0.05 | 0.30 | 10.94–11.38 | 3% |
| word-frequency | Marimay native | 0.63 | 1.30 | 144.57–148.02 | 2% |
| word-frequency | Go native | 0.26 | 0.53 | 18.58–19.75 | 4% |
| word-frequency | Rust native | 0.27 | 0.65 | 29.84–31.03 | 3% |
| report-builder | Marimay native | 0.12 | 0.37 | 14.56–15.38 | 2% |
| report-builder | Go native | 0.22 | 0.77 | 4.80–5.80 | 15% |
| report-builder | Rust native | 0.33 | 0.57 | 4.81–5.96 | 19% |
| report-concat | Marimay native | 0.65 | 0.96 | 97.21–99.93 | 2% |
| report-concat | Go native | 0.63 | 1.49 | 78.85–83.38 | 2% |
| report-concat | Rust native | 0.37 | 0.94 | 46.63–48.97 | 2% |
| map-int | Marimay native | 0.32 | 0.68 | 7.27–8.40 | 12% |
| map-int | Go native | 0.16 | 0.32 | 4.78–5.46 | 9% |
| map-int | Rust native | 0.36 | 0.63 | 5.42–6.52 | 18% |
| map-string | Marimay native | 0.17 | 0.52 | 22.82–23.75 | 2% |
| map-string | Go native | 0.16 | 0.40 | 6.89–9.07 | 7% |
| map-string | Rust native | 0.07 | 0.12 | 9.71–10.25 | 2% |
| map-string-book | Marimay native | 0.27 | 0.56 | 31.13–32.18 | 3% |
| map-string-book | Go native | 0.31 | 0.81 | 5.93–6.90 | 14% |
| map-string-book | Rust native | 0.24 | 0.48 | 10.08–11.03 | 7% |
| set-string-churn | Marimay native | 0.25 | 0.50 | 46.71–47.92 | 2% |
| set-string-churn | Go native | 0.14 | 0.26 | 9.44–10.44 | 4% |
| set-string-churn | Rust native | 0.20 | 0.37 | 16.77–17.45 | 4% |
| catalog-match | Marimay native | 0.06 | 0.19 | 13.06–13.67 | 2% |
| catalog-match | Go native | 0.32 | 0.65 | 4.45–5.24 | 20% |
| catalog-match | Rust native | 0.04 | 0.10 | 3.77–3.95 | 3% |
| catalog-dotcall | Marimay native | 0.13 | 0.23 | 8.09–8.79 | 5% |
| catalog-dotcall | Go native | 0.09 | 0.29 | 4.24–4.82 | 6% |
| catalog-dotcall | Rust native | 0.07 | 0.20 | 3.54–3.83 | 6% |
| catalog-interface | Marimay native | 0.17 | 0.28 | 11.74–12.88 | 4% |
| catalog-interface | Go native | 0.12 | 0.40 | 4.38–5.02 | 9% |
| catalog-interface | Rust native | 0.06 | 0.26 | 3.58–4.23 | 7% |
| record-reference-copy | Marimay native | 0.18 | 0.26 | 6.51–6.95 | 8% |
| record-reference-copy | Go native | 0.16 | 0.38 | 4.05–4.90 | 11% |
| record-reference-copy | Rust native | 0.03 | 0.07 | 3.07–3.44 | 3% |
| record-create | Marimay native | 0.14 | 0.54 | 22.85–23.94 | 2% |
| record-create | Go native | 0.32 | 0.65 | 6.42–7.28 | 14% |
| record-create | Rust native | 0.12 | 0.26 | 6.09–6.98 | 6% |
| array-grow | Marimay native | 0.09 | 0.21 | 6.51–6.90 | 4% |
| array-grow | Go native | 0.19 | 0.42 | 6.00–6.71 | 9% |
| array-grow | Rust native | 0.16 | 0.42 | 3.80–4.60 | 12% |
| array-reserved | Marimay native | 0.15 | 0.42 | 6.41–6.98 | 7% |
| array-reserved | Go native | 0.09 | 0.21 | 4.89–5.57 | 5% |
| array-reserved | Rust native | 0.04 | 0.28 | 3.75–4.28 | 7% |
| bfs-int | Marimay native | 0.05 | 0.18 | 7.19–7.49 | 2% |
| bfs-int | Go native | 0.13 | 0.46 | 4.86–5.41 | 9% |
| bfs-int | Rust native | 0.04 | 0.10 | 4.20–4.44 | 3% |
| bfs-record | Marimay native | 0.06 | 0.16 | 9.06–9.30 | 2% |
| bfs-record | Go native | 0.11 | 0.33 | 5.57–6.17 | 6% |
| bfs-record | Rust native | 0.11 | 0.24 | 4.40–4.75 | 7% |
| catalog-pipeline | Marimay native | 0.11 | 0.19 | 37.46–37.80 | 2% |
| catalog-pipeline | Go native | 0.15 | 0.40 | 7.60–8.46 | 6% |
| catalog-pipeline | Rust native | 0.05 | 0.11 | 9.82–10.31 | 2% |
| parse-result | Marimay native | 0.13 | 0.33 | 19.01–19.53 | 2% |
| parse-result | Go native | 0.19 | 0.48 | 5.66–6.40 | 10% |
| parse-result | Rust native | 0.08 | 0.19 | 5.59–6.34 | 4% |
| insertion | Marimay native | 1.02 | 2.17 | 47.00–51.43 | 6% |
| insertion | Go native | 0.16 | 0.36 | 28.81–29.81 | 2% |
| insertion | Rust native | 0.17 | 0.31 | 28.16–28.83 | 2% |
| heap-sort | Marimay native | 0.11 | 0.38 | 31.96–115.55 | 2% |
| heap-sort | Go native | 0.17 | 0.42 | 38.77–40.01 | 2% |
| heap-sort | Rust native | 0.13 | 0.51 | 22.03–30.26 | 2% |
| stack | Marimay native | 0.15 | 0.33 | 9.52–10.11 | 5% |
| stack | Go native | 0.23 | 0.56 | 13.97–15.51 | 5% |
| stack | Rust native | 0.12 | 0.26 | 8.76–9.30 | 4% |
| queue | Marimay native | 0.15 | 0.37 | 9.53–10.37 | 4% |
| queue | Go native | 0.22 | 0.55 | 14.09–15.13 | 5% |
| queue | Rust native | 0.06 | 0.14 | 8.78–9.16 | 2% |
| min-heap | Marimay native | 0.25 | 0.52 | 45.81–47.07 | 2% |
| min-heap | Go native | 0.24 | 0.79 | 53.51–55.44 | 2% |
| min-heap | Rust native | 0.23 | 0.61 | 29.27–30.80 | 2% |
| dsu | Marimay native | 0.16 | 0.32 | 29.65–30.25 | 2% |
| dsu | Go native | 0.32 | 0.66 | 23.98–25.02 | 4% |
| dsu | Rust native | 0.26 | 0.62 | 21.48–22.66 | 3% |
| bfs | Marimay native | 0.25 | 0.51 | 109.10–110.24 | 2% |
| bfs | Go native | 0.92 | 1.69 | 61.00–64.30 | 4% |
| bfs | Rust native | 0.10 | 0.22 | 23.39–24.05 | 2% |
| dijkstra | Marimay native | 0.13 | 0.30 | 41.33–41.94 | 2% |
| dijkstra | Go native | 0.50 | 0.80 | 40.85–42.31 | 4% |
| dijkstra | Rust native | 0.16 | 0.34 | 38.89–39.72 | 2% |
| frequency-map | Marimay native | 0.15 | 0.41 | 32.46–42.69 | 2% |
| frequency-map | Go native | 0.09 | 0.29 | 13.70–14.33 | 2% |
| frequency-map | Rust native | 2.37 | 7.51 | 13.37–24.79 | 45% |
| unique-set | Marimay native | 0.17 | 0.40 | 26.71–28.08 | 2% |
| unique-set | Go native | 0.24 | 0.36 | 15.97–16.77 | 4% |
| unique-set | Rust native | 0.09 | 0.19 | 19.06–19.69 | 2% |
| rune-frequency | Marimay native | 0.23 | 0.48 | 22.25–23.03 | 3% |
| rune-frequency | Go native | 0.24 | 0.67 | 5.53–6.57 | 12% |
| rune-frequency | Rust native | 0.12 | 0.26 | 5.81–6.54 | 6% |

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

Command: `./benchmarks/catalog_bench.py --anchors --engine native --samples 11 --warmups 3 --output benchmarks/results/comprehensive-native-scalar-flow-2026-09-09.md`
