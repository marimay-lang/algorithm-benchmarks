# Catalogue and language benchmark

Generated: 2026-09-09T15:23:20+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **11** after **3** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | native / Go | native / Rust | Go target | Assessment |
|---|---|---|---|---|---|---|---|---|
| title-search-10k | 10,000 × 128 | 9.14 | 4.20 | 4.36 | 2.18× | 2.10× | — | measured |
| title-search-100k | 100,000 × 128 | 82.34 | 15.36 | 18.25 | 5.36× | 4.51× | — | measured |
| normalize-title | 10,000 × 1 | 57.53 | 8.89 | 11.08 | 6.47× | 5.19× | — | measured |
| word-frequency | 10,000 × 10 | 145.88 | 19.03 | 30.45 | 7.67× | 4.79× | ≤ 2.0× | above target |
| report-builder | 10,000 × 1 | 14.75 | 5.17 | 5.18 | 2.85× | 2.85× | — | measured |
| report-concat | 10,000 × 1 | 97.60 | 81.31 | 47.84 | 1.20× | 2.04× | — | measured |
| map-int | 4,096 × 32 | 7.59 | 5.08 | 5.98 | 1.49× | 1.27× | ≤ 1.5× | within target |
| map-string | 4,096 × 32 | 23.16 | 7.47 | 9.87 | 3.10× | 2.35× | ≤ 2.0× | above target |
| map-string-book | 10,000 × 4 | 31.45 | 6.48 | 10.56 | 4.85× | 2.98× | — | measured |
| set-string-churn | 4,096 × 8 | 47.43 | 10.16 | 17.21 | 4.67× | 2.76× | — | measured |
| catalog-match | 10,000 × 32 | 13.27 | 5.05 | 3.82 | 2.63× | 3.47× | ≤ 1.5× | above target |
| catalog-dotcall | 10,000 × 32 | 8.31 | 4.47 | 3.74 | 1.86× | 2.22× | — | measured |
| catalog-interface | 10,000 × 32 | 12.04 | 4.82 | 3.72 | 2.50× | 3.23× | — | measured |
| record-reference-copy | 1,024 × 128 | 6.72 | 4.66 | 3.29 | 1.44× | 2.04× | — | measured |
| record-create | 1,024 × 128 | 23.26 | 6.93 | 6.31 | 3.35× | 3.69× | — | measured |
| array-grow | 100,000 × 4 | 6.66 | 6.35 | 4.17 | 1.05× | 1.60× | — | measured |
| array-reserved | 100,000 × 4 | 6.55 | 5.20 | 3.95 | 1.26× | 1.66× | — | measured |
| bfs-int | 4,096 × 16 | 7.33 | 5.18 | 4.27 | 1.41× | 1.72× | — | measured |
| bfs-record | 4,096 × 16 | 9.24 | 5.74 | 4.66 | 1.61× | 1.98× | — | measured |
| catalog-pipeline | 10,000 × 16 | 37.78 | 7.78 | 9.94 | 4.85× | 3.80× | — | measured |
| parse-result | 10,000 × 8 | 19.37 | 5.86 | 5.98 | 3.31× | 3.24× | — | measured |
| insertion | fixed anchor | 50.66 | 29.28 | 28.34 | 1.73× | 1.79× | — | measured |
| heap-sort | fixed anchor | 32.43 | 39.26 | 22.35 | 0.83× | 1.45× | ≤ 1.3× | within target |
| stack | fixed anchor | 10.06 | 14.84 | 8.94 | 0.68× | 1.13× | ≤ 1.3× | within target |
| queue | fixed anchor | 9.80 | 14.63 | 8.99 | 0.67× | 1.09× | ≤ 1.3× | within target |
| min-heap | fixed anchor | 46.24 | 53.74 | 29.45 | 0.86× | 1.57× | ≤ 1.3× | within target |
| dsu | fixed anchor | 29.75 | 24.68 | 21.84 | 1.21× | 1.36× | — | measured |
| bfs | fixed anchor | 65.72 | 63.39 | 23.87 | 1.04× | 2.75× | — | measured |
| dijkstra | fixed anchor | 41.57 | 41.73 | 39.48 | 1.00× | 1.05× | ≤ 1.3× | within target |
| frequency-map | fixed anchor | 32.79 | 14.18 | 23.32 | 2.31× | 1.41× | — | noisy; repeat |
| unique-set | fixed anchor | 27.07 | 16.45 | 19.25 | 1.64× | 1.41× | — | measured |
| rune-frequency | fixed anchor | 22.63 | 5.58 | 6.02 | 4.06× | 3.76× | — | measured |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.16 | 0.33 | 8.91–9.46 | 5% |
| title-search-10k | Go native | 0.14 | 0.56 | 3.97–5.45 | 13% |
| title-search-10k | Rust native | 0.15 | 0.29 | 4.08–4.63 | 10% |
| title-search-100k | Marimay native | 2.61 | 4.47 | 78.69–85.36 | 10% |
| title-search-100k | Go native | 0.31 | 0.64 | 14.74–16.04 | 6% |
| title-search-100k | Rust native | 0.20 | 0.44 | 17.87–19.07 | 3% |
| normalize-title | Marimay native | 0.31 | 0.71 | 56.91–59.48 | 2% |
| normalize-title | Go native | 0.41 | 0.83 | 8.12–9.82 | 14% |
| normalize-title | Rust native | 0.29 | 0.70 | 10.72–11.92 | 8% |
| word-frequency | Marimay native | 0.72 | 1.46 | 143.97–238.53 | 2% |
| word-frequency | Go native | 0.20 | 0.41 | 18.71–20.01 | 3% |
| word-frequency | Rust native | 0.28 | 0.64 | 29.89–30.77 | 3% |
| report-builder | Marimay native | 0.17 | 0.60 | 14.58–15.50 | 4% |
| report-builder | Go native | 0.32 | 0.79 | 4.66–5.81 | 19% |
| report-builder | Rust native | 0.21 | 0.53 | 4.91–5.96 | 12% |
| report-concat | Marimay native | 0.64 | 1.49 | 96.61–102.03 | 2% |
| report-concat | Go native | 1.86 | 4.17 | 79.15–84.22 | 7% |
| report-concat | Rust native | 0.53 | 1.54 | 46.73–50.40 | 3% |
| map-int | Marimay native | 0.12 | 0.62 | 7.32–8.72 | 8% |
| map-int | Go native | 0.13 | 0.27 | 4.79–5.28 | 8% |
| map-int | Rust native | 0.22 | 0.52 | 5.75–6.80 | 11% |
| map-string | Marimay native | 0.26 | 0.47 | 22.71–23.66 | 3% |
| map-string | Go native | 0.21 | 0.48 | 7.05–8.18 | 8% |
| map-string | Rust native | 0.15 | 0.30 | 9.61–10.10 | 5% |
| map-string-book | Marimay native | 0.12 | 0.30 | 31.06–31.93 | 2% |
| map-string-book | Go native | 0.14 | 0.35 | 6.06–7.50 | 7% |
| map-string-book | Rust native | 0.17 | 0.21 | 10.24–11.16 | 5% |
| set-string-churn | Marimay native | 0.29 | 0.56 | 46.69–48.49 | 2% |
| set-string-churn | Go native | 0.21 | 0.46 | 9.80–10.71 | 6% |
| set-string-churn | Rust native | 0.28 | 0.70 | 16.62–18.03 | 5% |
| catalog-match | Marimay native | 0.11 | 0.23 | 12.93–13.70 | 3% |
| catalog-match | Go native | 0.49 | 1.02 | 4.25–5.55 | 29% |
| catalog-match | Rust native | 0.08 | 0.15 | 3.67–3.98 | 6% |
| catalog-dotcall | Marimay native | 0.08 | 0.26 | 8.23–8.86 | 3% |
| catalog-dotcall | Go native | 0.16 | 0.40 | 4.31–5.22 | 11% |
| catalog-dotcall | Rust native | 0.03 | 0.06 | 3.55–3.94 | 2% |
| catalog-interface | Marimay native | 0.04 | 0.07 | 11.93–12.84 | 2% |
| catalog-interface | Go native | 0.12 | 0.30 | 4.35–4.99 | 8% |
| catalog-interface | Rust native | 0.05 | 0.11 | 3.62–4.28 | 4% |
| record-reference-copy | Marimay native | 0.03 | 0.08 | 6.63–7.13 | 2% |
| record-reference-copy | Go native | 0.24 | 0.62 | 4.16–5.42 | 16% |
| record-reference-copy | Rust native | 0.06 | 0.16 | 3.18–3.56 | 6% |
| record-create | Marimay native | 0.20 | 0.38 | 22.88–23.60 | 3% |
| record-create | Go native | 0.10 | 0.29 | 6.55–7.09 | 4% |
| record-create | Rust native | 0.12 | 0.22 | 6.05–6.73 | 6% |
| array-grow | Marimay native | 0.11 | 0.20 | 6.50–6.88 | 5% |
| array-grow | Go native | 0.05 | 0.19 | 6.21–6.66 | 3% |
| array-grow | Rust native | 0.17 | 0.36 | 4.00–4.60 | 12% |
| array-reserved | Marimay native | 0.08 | 0.16 | 6.43–6.85 | 4% |
| array-reserved | Go native | 0.16 | 0.36 | 4.98–5.72 | 9% |
| array-reserved | Rust native | 0.10 | 0.23 | 3.78–4.35 | 7% |
| bfs-int | Marimay native | 0.16 | 0.30 | 7.14–7.62 | 6% |
| bfs-int | Go native | 0.10 | 0.21 | 5.08–5.57 | 6% |
| bfs-int | Rust native | 0.04 | 0.17 | 4.19–4.63 | 4% |
| bfs-record | Marimay native | 0.11 | 0.26 | 9.13–9.76 | 4% |
| bfs-record | Go native | 0.08 | 0.25 | 5.58–6.14 | 4% |
| bfs-record | Rust native | 0.08 | 0.16 | 4.50–4.95 | 5% |
| catalog-pipeline | Marimay native | 0.14 | 0.29 | 37.33–38.22 | 2% |
| catalog-pipeline | Go native | 0.13 | 0.29 | 7.51–8.26 | 5% |
| catalog-pipeline | Rust native | 0.04 | 0.10 | 9.81–10.07 | 2% |
| parse-result | Marimay native | 0.07 | 0.30 | 18.94–19.78 | 2% |
| parse-result | Go native | 0.16 | 0.30 | 5.65–6.46 | 8% |
| parse-result | Rust native | 0.28 | 0.66 | 5.59–6.42 | 14% |
| insertion | Marimay native | 1.44 | 3.43 | 47.72–131.71 | 9% |
| insertion | Go native | 0.14 | 0.34 | 28.81–29.96 | 2% |
| insertion | Rust native | 0.08 | 0.20 | 28.13–29.46 | 2% |
| heap-sort | Marimay native | 0.16 | 0.32 | 32.14–32.99 | 2% |
| heap-sort | Go native | 0.25 | 0.38 | 38.76–53.46 | 2% |
| heap-sort | Rust native | 0.29 | 0.62 | 22.04–22.89 | 4% |
| stack | Marimay native | 0.15 | 0.34 | 9.67–10.37 | 5% |
| stack | Go native | 0.26 | 0.53 | 14.36–15.40 | 5% |
| stack | Rust native | 0.09 | 0.24 | 8.69–9.17 | 3% |
| queue | Marimay native | 0.11 | 0.17 | 9.53–10.36 | 3% |
| queue | Go native | 0.16 | 0.40 | 14.33–15.27 | 3% |
| queue | Rust native | 0.15 | 0.40 | 8.68–9.54 | 5% |
| min-heap | Marimay native | 0.25 | 0.60 | 45.93–47.27 | 2% |
| min-heap | Go native | 0.19 | 0.84 | 53.40–54.61 | 2% |
| min-heap | Rust native | 0.12 | 0.75 | 29.06–30.71 | 3% |
| dsu | Marimay native | 0.08 | 0.27 | 29.67–30.09 | 2% |
| dsu | Go native | 0.20 | 0.66 | 24.04–25.13 | 3% |
| dsu | Rust native | 0.11 | 0.28 | 21.64–22.23 | 2% |
| bfs | Marimay native | 0.41 | 0.78 | 65.17–66.65 | 2% |
| bfs | Go native | 0.71 | 1.79 | 61.28–64.09 | 3% |
| bfs | Rust native | 0.13 | 0.26 | 23.59–24.44 | 2% |
| dijkstra | Marimay native | 0.15 | 0.50 | 41.40–43.03 | 2% |
| dijkstra | Go native | 0.40 | 0.91 | 41.04–43.07 | 3% |
| dijkstra | Rust native | 0.30 | 0.82 | 39.05–41.87 | 2% |
| frequency-map | Marimay native | 0.22 | 0.76 | 32.32–34.31 | 2% |
| frequency-map | Go native | 0.12 | 0.29 | 13.55–16.27 | 3% |
| frequency-map | Rust native | 1.62 | 8.00 | 14.26–25.20 | 34% |
| unique-set | Marimay native | 0.12 | 0.25 | 26.84–27.65 | 2% |
| unique-set | Go native | 0.18 | 0.55 | 15.79–16.97 | 3% |
| unique-set | Rust native | 0.18 | 0.36 | 18.87–19.67 | 3% |
| rune-frequency | Marimay native | 0.27 | 0.53 | 22.27–23.18 | 4% |
| rune-frequency | Go native | 0.12 | 0.45 | 5.40–6.44 | 8% |
| rune-frequency | Rust native | 0.11 | 0.15 | 5.79–6.90 | 5% |

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

Command: `./benchmarks/catalog_bench.py --anchors --engine native --samples 11 --warmups 3 --output benchmarks/results/comprehensive-native-scalar-flow-final-2026-09-09.md`
