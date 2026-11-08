# Catalogue and language benchmark

Generated: 2026-09-09T12:13:40+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **11** after **3** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | native / Go | native / Rust | Go target | Assessment |
|---|---|---|---|---|---|---|---|---|
| title-search-10k | 10,000 × 128 | 8.82 | 4.04 | 4.08 | 2.18× | 2.16× | — | measured |
| title-search-100k | 100,000 × 128 | 71.50 | 14.47 | 17.50 | 4.94× | 4.09× | — | measured |
| normalize-title | 10,000 × 1 | 55.87 | 8.58 | 10.55 | 6.51× | 5.30× | — | measured |
| word-frequency | 10,000 × 10 | 135.36 | 18.53 | 29.84 | 7.31× | 4.54× | ≤ 2.0× | above target |
| report-builder | 10,000 × 1 | 14.06 | 4.82 | 4.86 | 2.92× | 2.89× | — | measured |
| report-concat | 10,000 × 1 | 93.65 | 79.45 | 46.20 | 1.18× | 2.03× | — | measured |
| map-int | 4,096 × 32 | 7.31 | 4.74 | 5.58 | 1.54× | 1.31× | ≤ 1.5× | above target |
| map-string | 4,096 × 32 | 22.48 | 7.05 | 9.51 | 3.19× | 2.36× | ≤ 2.0× | above target |
| map-string-book | 10,000 × 4 | 30.36 | 6.13 | 10.06 | 4.95× | 3.02× | — | measured |
| set-string-churn | 4,096 × 8 | 45.66 | 9.67 | 16.73 | 4.72× | 2.73× | — | measured |
| catalog-match | 10,000 × 32 | 13.69 | 4.42 | 3.65 | 3.10× | 3.76× | ≤ 1.5× | above target |
| catalog-dotcall | 10,000 × 32 | 8.05 | 4.30 | 3.57 | 1.87× | 2.26× | — | measured |
| catalog-interface | 10,000 × 32 | 11.71 | 4.55 | 3.58 | 2.57× | 3.27× | — | measured |
| record-reference-copy | 1,024 × 128 | 8.28 | 4.32 | 3.19 | 1.92× | 2.59× | — | measured |
| record-create | 1,024 × 128 | 23.83 | 6.38 | 6.14 | 3.73× | 3.88× | — | measured |
| array-grow | 100,000 × 4 | 6.61 | 6.09 | 3.82 | 1.09× | 1.73× | — | measured |
| array-reserved | 100,000 × 4 | 6.52 | 4.94 | 4.01 | 1.32× | 1.63× | — | measured |
| bfs-int | 4,096 × 16 | 7.27 | 4.98 | 4.17 | 1.46× | 1.74× | — | measured |
| bfs-record | 4,096 × 16 | 553.85 | 5.67 | 4.54 | 97.70× | 122.05× | — | measured |
| catalog-pipeline | 10,000 × 16 | 38.82 | 7.51 | 9.71 | 5.17× | 4.00× | — | measured |
| parse-result | 10,000 × 8 | 18.68 | 5.55 | 5.74 | 3.37× | 3.25× | — | measured |
| insertion | fixed anchor | 51.96 | 28.77 | 27.85 | 1.81× | 1.87× | — | measured |
| heap-sort | fixed anchor | 31.62 | 38.50 | 21.68 | 0.82× | 1.46× | ≤ 1.3× | within target |
| stack | fixed anchor | 9.23 | 13.89 | 8.57 | 0.66× | 1.08× | ≤ 1.3× | within target |
| queue | fixed anchor | 9.34 | 14.07 | 8.70 | 0.66× | 1.07× | ≤ 1.3× | within target |
| min-heap | fixed anchor | 41.56 | 52.46 | 28.50 | 0.79× | 1.46× | ≤ 1.3× | within target |
| dsu | fixed anchor | 29.33 | 24.06 | 21.39 | 1.22× | 1.37× | — | measured |
| bfs | fixed anchor | 60.69 | 62.18 | 23.15 | 0.98× | 2.62× | — | measured |
| dijkstra | fixed anchor | 38.50 | 40.93 | 38.69 | 0.94× | 0.99× | ≤ 1.3× | within target |
| frequency-map | fixed anchor | 32.29 | 13.46 | 22.88 | 2.40× | 1.41× | — | noisy; repeat |
| unique-set | fixed anchor | 26.57 | 15.69 | 17.97 | 1.69× | 1.48× | — | measured |
| rune-frequency | fixed anchor | 22.06 | 5.65 | 5.93 | 3.90× | 3.72× | — | measured |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.08 | 0.16 | 8.70–9.20 | 3% |
| title-search-10k | Go native | 0.10 | 0.21 | 3.89–4.74 | 8% |
| title-search-10k | Rust native | 0.05 | 0.07 | 3.97–4.48 | 4% |
| title-search-100k | Marimay native | 1.41 | 2.61 | 69.52–73.10 | 6% |
| title-search-100k | Go native | 0.32 | 0.69 | 13.98–14.99 | 7% |
| title-search-100k | Rust native | 0.08 | 0.17 | 17.32–17.73 | 2% |
| normalize-title | Marimay native | 0.19 | 0.48 | 55.52–56.82 | 2% |
| normalize-title | Go native | 0.24 | 0.37 | 7.82–9.25 | 8% |
| normalize-title | Rust native | 0.07 | 0.15 | 10.38–10.97 | 2% |
| word-frequency | Marimay native | 0.33 | 0.69 | 134.94–136.04 | 2% |
| word-frequency | Go native | 0.09 | 0.18 | 18.09–18.74 | 2% |
| word-frequency | Rust native | 0.25 | 0.53 | 29.51–30.39 | 3% |
| report-builder | Marimay native | 0.08 | 0.17 | 13.85–14.38 | 2% |
| report-builder | Go native | 0.20 | 0.43 | 4.50–5.39 | 13% |
| report-builder | Rust native | 0.07 | 0.36 | 4.74–5.56 | 7% |
| report-concat | Marimay native | 0.38 | 0.92 | 92.52–94.26 | 2% |
| report-concat | Go native | 0.67 | 2.35 | 77.57–82.42 | 3% |
| report-concat | Rust native | 0.19 | 0.58 | 45.60–46.64 | 2% |
| map-int | Marimay native | 0.12 | 0.25 | 7.12–7.74 | 5% |
| map-int | Go native | 0.12 | 0.24 | 4.44–5.02 | 8% |
| map-int | Rust native | 0.06 | 0.41 | 5.35–6.12 | 7% |
| map-string | Marimay native | 0.06 | 0.16 | 22.22–22.63 | 2% |
| map-string | Go native | 0.12 | 0.31 | 6.85–7.20 | 5% |
| map-string | Rust native | 0.04 | 0.07 | 8.86–9.62 | 2% |
| map-string-book | Marimay native | 0.03 | 0.06 | 30.23–30.57 | 2% |
| map-string-book | Go native | 0.16 | 0.22 | 5.82–6.42 | 8% |
| map-string-book | Rust native | 0.13 | 0.30 | 9.71–10.27 | 4% |
| set-string-churn | Marimay native | 0.25 | 0.56 | 45.21–46.07 | 2% |
| set-string-churn | Go native | 0.09 | 0.25 | 9.50–9.98 | 3% |
| set-string-churn | Rust native | 0.09 | 0.35 | 16.40–17.02 | 2% |
| catalog-match | Marimay native | 0.05 | 0.20 | 13.65–13.95 | 2% |
| catalog-match | Go native | 0.30 | 0.64 | 4.08–4.95 | 21% |
| catalog-match | Rust native | 0.08 | 0.18 | 3.54–3.79 | 7% |
| catalog-dotcall | Marimay native | 0.06 | 0.14 | 7.89–8.15 | 2% |
| catalog-dotcall | Go native | 0.11 | 0.26 | 4.15–4.65 | 8% |
| catalog-dotcall | Rust native | 0.08 | 0.12 | 3.39–4.95 | 7% |
| catalog-interface | Marimay native | 0.11 | 0.26 | 11.58–12.31 | 3% |
| catalog-interface | Go native | 0.17 | 0.26 | 4.22–4.72 | 11% |
| catalog-interface | Rust native | 0.02 | 0.04 | 3.47–3.70 | 2% |
| record-reference-copy | Marimay native | 0.11 | 0.18 | 8.11–8.55 | 4% |
| record-reference-copy | Go native | 0.14 | 0.28 | 4.10–4.58 | 10% |
| record-reference-copy | Rust native | 0.08 | 0.16 | 3.08–3.35 | 7% |
| record-create | Marimay native | 0.10 | 0.32 | 23.56–24.22 | 2% |
| record-create | Go native | 0.11 | 0.24 | 6.17–7.07 | 5% |
| record-create | Rust native | 0.13 | 0.24 | 5.96–6.43 | 6% |
| array-grow | Marimay native | 0.07 | 0.19 | 6.43–6.78 | 3% |
| array-grow | Go native | 0.11 | 0.27 | 5.78–6.33 | 5% |
| array-grow | Rust native | 0.12 | 0.40 | 3.63–4.25 | 10% |
| array-reserved | Marimay native | 0.06 | 0.23 | 6.43–6.72 | 3% |
| array-reserved | Go native | 0.09 | 0.25 | 4.75–5.18 | 6% |
| array-reserved | Rust native | 0.06 | 0.12 | 3.75–4.20 | 4% |
| bfs-int | Marimay native | 0.05 | 0.11 | 7.17–7.38 | 2% |
| bfs-int | Go native | 0.12 | 0.26 | 4.82–5.37 | 7% |
| bfs-int | Rust native | 0.04 | 0.16 | 4.09–4.48 | 4% |
| bfs-record | Marimay native | 0.63 | 2.17 | 551.27–563.06 | 2% |
| bfs-record | Go native | 0.27 | 0.54 | 5.26–6.14 | 14% |
| bfs-record | Rust native | 0.09 | 0.24 | 4.35–5.42 | 6% |
| catalog-pipeline | Marimay native | 0.06 | 0.13 | 38.56–38.89 | 2% |
| catalog-pipeline | Go native | 0.07 | 0.34 | 7.38–7.92 | 5% |
| catalog-pipeline | Rust native | 0.03 | 0.08 | 9.68–9.79 | 2% |
| parse-result | Marimay native | 0.07 | 0.19 | 18.47–19.25 | 2% |
| parse-result | Go native | 0.07 | 0.20 | 5.37–5.81 | 4% |
| parse-result | Rust native | 0.06 | 0.14 | 5.52–5.92 | 3% |
| insertion | Marimay native | 0.43 | 1.28 | 48.56–52.46 | 2% |
| insertion | Go native | 0.20 | 0.44 | 28.34–30.25 | 2% |
| insertion | Rust native | 0.11 | 0.25 | 27.72–28.19 | 2% |
| heap-sort | Marimay native | 0.06 | 0.13 | 31.49–31.76 | 2% |
| heap-sort | Go native | 0.21 | 0.39 | 38.18–39.50 | 2% |
| heap-sort | Rust native | 0.09 | 0.29 | 21.58–29.71 | 2% |
| stack | Marimay native | 0.07 | 0.18 | 9.11–9.54 | 2% |
| stack | Go native | 0.19 | 0.54 | 13.59–14.53 | 4% |
| stack | Rust native | 0.10 | 0.19 | 8.43–8.86 | 3% |
| queue | Marimay native | 0.18 | 0.30 | 9.13–10.48 | 6% |
| queue | Go native | 0.14 | 0.32 | 13.66–14.81 | 3% |
| queue | Rust native | 0.07 | 0.21 | 8.28–9.05 | 3% |
| min-heap | Marimay native | 0.02 | 0.22 | 41.54–42.26 | 2% |
| min-heap | Go native | 0.22 | 0.46 | 51.99–53.03 | 2% |
| min-heap | Rust native | 0.08 | 0.15 | 28.32–28.97 | 2% |
| dsu | Marimay native | 0.13 | 0.33 | 29.20–29.93 | 2% |
| dsu | Go native | 0.04 | 0.22 | 23.62–24.98 | 2% |
| dsu | Rust native | 0.12 | 0.23 | 21.04–21.57 | 2% |
| bfs | Marimay native | 0.24 | 0.50 | 60.09–61.88 | 2% |
| bfs | Go native | 0.78 | 1.66 | 60.58–63.56 | 4% |
| bfs | Rust native | 0.22 | 0.33 | 22.82–23.62 | 3% |
| dijkstra | Marimay native | 0.11 | 0.26 | 38.05–39.19 | 2% |
| dijkstra | Go native | 0.41 | 0.78 | 39.80–41.74 | 3% |
| dijkstra | Rust native | 0.13 | 0.23 | 38.48–39.61 | 2% |
| frequency-map | Marimay native | 0.15 | 0.38 | 31.80–32.73 | 2% |
| frequency-map | Go native | 0.11 | 0.30 | 13.29–13.96 | 3% |
| frequency-map | Rust native | 2.02 | 8.55 | 13.28–24.90 | 37% |
| unique-set | Marimay native | 0.05 | 0.10 | 26.32–26.79 | 2% |
| unique-set | Go native | 0.13 | 0.28 | 15.51–16.03 | 2% |
| unique-set | Rust native | 0.08 | 0.27 | 17.75–18.48 | 2% |
| rune-frequency | Marimay native | 0.14 | 0.29 | 21.82–22.28 | 2% |
| rune-frequency | Go native | 0.08 | 0.49 | 5.31–6.26 | 9% |
| rune-frequency | Rust native | 0.17 | 0.72 | 5.73–6.69 | 12% |

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

Command: `./benchmarks/catalog_bench.py --anchors --engine native --samples 11 --warmups 3 --output benchmarks/results/comprehensive-native-fc754a8-2026-09-09.md`
