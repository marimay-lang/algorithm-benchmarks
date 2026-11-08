# Catalogue and language benchmark

Generated: 2026-09-09T12:38:19+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **11** after **3** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | native / Go | native / Rust | Go target | Assessment |
|---|---|---|---|---|---|---|---|---|
| title-search-10k | 10,000 × 128 | 9.55 | 4.71 | 4.41 | 2.03× | 2.17× | — | measured |
| title-search-100k | 100,000 × 128 | 81.68 | 15.72 | 19.56 | 5.20× | 4.18× | — | measured |
| normalize-title | 10,000 × 1 | 60.63 | 9.83 | 11.68 | 6.17× | 5.19× | — | measured |
| word-frequency | 10,000 × 10 | 143.12 | 20.11 | 31.50 | 7.12× | 4.54× | ≤ 2.0× | above target |
| report-builder | 10,000 × 1 | 15.91 | 5.50 | 5.60 | 2.89× | 2.84× | — | measured |
| report-concat | 10,000 × 1 | 108.37 | 84.94 | 51.66 | 1.28× | 2.10× | — | measured |
| map-int | 4,096 × 32 | 8.09 | 5.33 | 6.43 | 1.52× | 1.26× | ≤ 1.5× | above target |
| map-string | 4,096 × 32 | 25.06 | 8.15 | 11.10 | 3.08× | 2.26× | ≤ 2.0× | above target |
| map-string-book | 10,000 × 4 | 34.03 | 7.55 | 11.65 | 4.50× | 2.92× | — | measured |
| set-string-churn | 4,096 × 8 | 52.18 | 10.96 | 19.35 | 4.76× | 2.70× | — | measured |
| catalog-match | 10,000 × 32 | 14.63 | 5.34 | 4.39 | 2.74× | 3.33× | ≤ 1.5× | above target |
| catalog-dotcall | 10,000 × 32 | 8.18 | 5.14 | 3.89 | 1.59× | 2.10× | — | measured |
| catalog-interface | 10,000 × 32 | 12.63 | 5.00 | 4.25 | 2.53× | 2.97× | — | measured |
| record-reference-copy | 1,024 × 128 | 7.18 | 5.13 | 3.83 | 1.40× | 1.87× | — | noisy; repeat |
| record-create | 1,024 × 128 | 24.38 | 7.49 | 6.65 | 3.26× | 3.67× | — | measured |
| array-grow | 100,000 × 4 | 7.07 | 6.50 | 4.70 | 1.09× | 1.50× | — | measured |
| array-reserved | 100,000 × 4 | 6.92 | 5.65 | 4.14 | 1.22× | 1.67× | — | measured |
| bfs-int | 4,096 × 16 | 7.50 | 5.65 | 4.67 | 1.33× | 1.61× | — | measured |
| bfs-record | 4,096 × 16 | 9.58 | 6.80 | 4.79 | 1.41× | 2.00× | — | measured |
| catalog-pipeline | 10,000 × 16 | 38.28 | 8.42 | 10.47 | 4.54× | 3.66× | — | measured |
| parse-result | 10,000 × 8 | 19.97 | 6.19 | 6.45 | 3.22× | 3.10× | — | measured |
| insertion | fixed anchor | 51.59 | 30.28 | 29.53 | 1.70× | 1.75× | — | measured |
| heap-sort | fixed anchor | 34.25 | 40.92 | 23.67 | 0.84× | 1.45× | ≤ 1.3× | within target |
| stack | fixed anchor | 10.08 | 15.72 | 9.32 | 0.64× | 1.08× | ≤ 1.3× | within target |
| queue | fixed anchor | 10.74 | 16.03 | 9.42 | 0.67× | 1.14× | ≤ 1.3× | within target |
| min-heap | fixed anchor | 45.79 | 57.19 | 32.17 | 0.80× | 1.42× | ≤ 1.3× | within target |
| dsu | fixed anchor | 30.83 | 25.46 | 23.03 | 1.21× | 1.34× | — | measured |
| bfs | fixed anchor | 66.81 | 64.27 | 25.24 | 1.04× | 2.65× | — | measured |
| dijkstra | fixed anchor | 41.17 | 44.01 | 41.20 | 0.94× | 1.00× | ≤ 1.3× | within target |
| frequency-map | fixed anchor | 33.65 | 14.77 | 21.27 | 2.28× | 1.58× | — | noisy; repeat |
| unique-set | fixed anchor | 28.32 | 17.35 | 21.11 | 1.63× | 1.34× | — | measured |
| rune-frequency | fixed anchor | 23.77 | 6.26 | 6.75 | 3.79× | 3.52× | — | measured |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.27 | 1.06 | 9.27–12.30 | 11% |
| title-search-10k | Go native | 0.36 | 0.87 | 4.13–5.74 | 23% |
| title-search-10k | Rust native | 0.14 | 0.53 | 4.20–5.10 | 12% |
| title-search-100k | Marimay native | 1.96 | 5.23 | 75.25–90.78 | 7% |
| title-search-100k | Go native | 0.44 | 1.19 | 15.19–17.54 | 8% |
| title-search-100k | Rust native | 0.79 | 1.61 | 18.23–22.00 | 12% |
| normalize-title | Marimay native | 2.37 | 4.90 | 57.25–70.50 | 12% |
| normalize-title | Go native | 0.50 | 0.86 | 8.59–10.67 | 15% |
| normalize-title | Rust native | 0.33 | 0.50 | 10.92–12.55 | 9% |
| word-frequency | Marimay native | 0.99 | 3.25 | 139.54–150.28 | 2% |
| word-frequency | Go native | 0.30 | 0.71 | 19.61–22.28 | 4% |
| word-frequency | Rust native | 0.54 | 1.92 | 30.33–46.93 | 6% |
| report-builder | Marimay native | 0.37 | 0.90 | 15.12–17.80 | 7% |
| report-builder | Go native | 0.21 | 0.49 | 4.89–6.06 | 12% |
| report-builder | Rust native | 0.23 | 0.75 | 4.96–6.20 | 13% |
| report-concat | Marimay native | 3.42 | 6.22 | 103.72–116.66 | 9% |
| report-concat | Go native | 1.27 | 3.63 | 83.26–91.43 | 4% |
| report-concat | Rust native | 1.56 | 3.31 | 50.10–58.55 | 9% |
| map-int | Marimay native | 0.41 | 0.98 | 7.46–9.05 | 15% |
| map-int | Go native | 0.19 | 0.57 | 4.77–7.00 | 11% |
| map-int | Rust native | 0.35 | 0.81 | 5.75–7.48 | 16% |
| map-string | Marimay native | 1.17 | 2.06 | 23.67–27.76 | 14% |
| map-string | Go native | 0.39 | 0.81 | 7.14–8.68 | 14% |
| map-string | Rust native | 0.50 | 0.98 | 10.16–13.11 | 13% |
| map-string-book | Marimay native | 0.68 | 1.41 | 32.55–35.29 | 6% |
| map-string-book | Go native | 0.40 | 0.77 | 6.69–8.56 | 16% |
| map-string-book | Rust native | 0.71 | 1.26 | 10.30–12.76 | 18% |
| set-string-churn | Marimay native | 0.53 | 3.38 | 47.84–55.57 | 6% |
| set-string-churn | Go native | 0.83 | 1.24 | 9.78–12.09 | 23% |
| set-string-churn | Rust native | 0.50 | 1.59 | 17.37–36.58 | 8% |
| catalog-match | Marimay native | 0.68 | 1.56 | 13.49–15.96 | 14% |
| catalog-match | Go native | 0.38 | 0.75 | 4.30–6.54 | 21% |
| catalog-match | Rust native | 0.40 | 0.87 | 3.56–5.16 | 27% |
| catalog-dotcall | Marimay native | 0.23 | 0.47 | 7.78–9.34 | 8% |
| catalog-dotcall | Go native | 0.42 | 1.14 | 4.59–6.28 | 25% |
| catalog-dotcall | Rust native | 0.21 | 0.75 | 3.58–4.81 | 19% |
| catalog-interface | Marimay native | 0.22 | 0.43 | 11.73–13.86 | 5% |
| catalog-interface | Go native | 0.21 | 0.84 | 4.40–5.77 | 17% |
| catalog-interface | Rust native | 0.20 | 0.57 | 3.69–4.63 | 14% |
| record-reference-copy | Marimay native | 0.27 | 0.66 | 6.83–7.58 | 11% |
| record-reference-copy | Go native | 0.57 | 1.16 | 4.37–6.50 | 33% |
| record-reference-copy | Rust native | 0.37 | 0.57 | 3.16–4.23 | 29% |
| record-create | Marimay native | 0.74 | 1.74 | 23.16–26.44 | 9% |
| record-create | Go native | 0.39 | 0.85 | 6.61–8.74 | 16% |
| record-create | Rust native | 0.42 | 0.83 | 6.14–8.08 | 19% |
| array-grow | Marimay native | 0.17 | 0.43 | 6.64–13.98 | 7% |
| array-grow | Go native | 0.20 | 1.18 | 6.19–9.39 | 18% |
| array-grow | Rust native | 0.26 | 0.58 | 4.06–8.85 | 16% |
| array-reserved | Marimay native | 0.18 | 0.82 | 6.70–11.14 | 12% |
| array-reserved | Go native | 0.25 | 0.56 | 4.97–10.66 | 13% |
| array-reserved | Rust native | 0.24 | 1.08 | 3.81–8.53 | 26% |
| bfs-int | Marimay native | 0.12 | 1.25 | 7.38–9.76 | 17% |
| bfs-int | Go native | 0.16 | 1.31 | 5.14–7.54 | 23% |
| bfs-int | Rust native | 0.26 | 0.89 | 4.23–5.59 | 19% |
| bfs-record | Marimay native | 0.33 | 1.29 | 9.16–13.31 | 13% |
| bfs-record | Go native | 0.46 | 1.12 | 5.71–29.33 | 20% |
| bfs-record | Rust native | 0.18 | 0.84 | 4.57–6.36 | 18% |
| catalog-pipeline | Marimay native | 0.56 | 4.90 | 37.58–43.98 | 13% |
| catalog-pipeline | Go native | 0.45 | 1.49 | 7.54–10.79 | 18% |
| catalog-pipeline | Rust native | 0.44 | 2.68 | 9.87–29.38 | 26% |
| parse-result | Marimay native | 0.79 | 1.59 | 18.99–22.17 | 12% |
| parse-result | Go native | 0.36 | 0.70 | 5.70–8.97 | 18% |
| parse-result | Rust native | 0.42 | 0.99 | 5.81–7.58 | 19% |
| insertion | Marimay native | 0.97 | 2.07 | 49.81–56.68 | 6% |
| insertion | Go native | 0.64 | 1.57 | 29.18–38.72 | 6% |
| insertion | Rust native | 0.76 | 1.45 | 28.27–43.41 | 8% |
| heap-sort | Marimay native | 1.46 | 3.04 | 32.30–37.59 | 13% |
| heap-sort | Go native | 1.50 | 3.26 | 39.15–69.64 | 11% |
| heap-sort | Rust native | 1.15 | 2.77 | 22.15–27.59 | 15% |
| stack | Marimay native | 0.20 | 0.85 | 9.65–12.50 | 8% |
| stack | Go native | 0.45 | 0.94 | 14.75–25.95 | 9% |
| stack | Rust native | 0.39 | 1.19 | 8.70–10.76 | 13% |
| queue | Marimay native | 0.51 | 1.38 | 10.07–17.58 | 14% |
| queue | Go native | 0.39 | 1.02 | 14.53–103.66 | 7% |
| queue | Rust native | 0.23 | 0.76 | 9.07–11.93 | 8% |
| min-heap | Marimay native | 2.81 | 5.10 | 42.83–77.19 | 18% |
| min-heap | Go native | 1.92 | 4.75 | 54.54–87.02 | 10% |
| min-heap | Rust native | 1.39 | 2.73 | 29.80–41.93 | 13% |
| dsu | Marimay native | 0.92 | 2.07 | 29.80–40.09 | 9% |
| dsu | Go native | 0.44 | 1.01 | 24.08–26.79 | 5% |
| dsu | Rust native | 0.52 | 1.05 | 21.52–24.47 | 7% |
| bfs | Marimay native | 1.45 | 2.33 | 63.63–85.88 | 6% |
| bfs | Go native | 2.18 | 4.18 | 61.59–68.35 | 10% |
| bfs | Rust native | 0.46 | 0.91 | 23.88–25.90 | 6% |
| dijkstra | Marimay native | 1.47 | 3.52 | 39.28–43.74 | 11% |
| dijkstra | Go native | 0.64 | 2.00 | 40.75–44.84 | 5% |
| dijkstra | Rust native | 1.23 | 2.03 | 39.06–42.43 | 9% |
| frequency-map | Marimay native | 0.57 | 0.95 | 32.77–36.60 | 5% |
| frequency-map | Go native | 0.56 | 1.38 | 14.16–16.05 | 11% |
| frequency-map | Rust native | 2.23 | 4.08 | 15.36–24.90 | 31% |
| unique-set | Marimay native | 1.13 | 2.29 | 27.18–31.92 | 12% |
| unique-set | Go native | 0.58 | 1.27 | 16.15–20.44 | 10% |
| unique-set | Rust native | 1.30 | 2.56 | 19.13–23.32 | 18% |
| rune-frequency | Marimay native | 0.52 | 0.94 | 22.26–45.79 | 7% |
| rune-frequency | Go native | 0.30 | 0.50 | 5.93–8.04 | 14% |
| rune-frequency | Rust native | 0.34 | 0.96 | 5.88–7.79 | 15% |

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

Command: `./benchmarks/catalog_bench.py --anchors --engine native --samples 11 --warmups 3 --output benchmarks/results/comprehensive-native-array-children-2026-09-09.md`
