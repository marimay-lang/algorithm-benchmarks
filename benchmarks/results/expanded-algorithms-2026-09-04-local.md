# Expanded local algorithm benchmark

Generated: `2026-09-04T23:54:21+07:00`

Host: `Darwin 25.6.0 arm64`; CPU: `Apple M2`.

Marimay compiler executable: `/path/to/Marimay/marimay/build/release/mmay`.

Marimay source revision: `7add961f51d70a988910a470c4da6c3604cef4ba`.

Algorithm corpus revision: `3eda6055ff56be328c775c79d4a26ca412af66fb`.

Equivalence manifest: `benchmarks/equivalence.json` (`64ddc892dcac9a30a9e4b86aa669d1dff5a12aea65c3f353e180958f23a8c27a`).

Expanded workload manifest: `benchmarks/expanded_workloads.json` (`ef6e688152b4bfe2906dd7ef22f285fc8a94d900d90c8518b0698a4da1aa1188`).

This extended matrix is local-only and is excluded from Tier 1 baselines.

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 52.87 ms | 31.39 ms | 31.86 ms | 1.7× | 1.7× | Go |
| heap-sort | 5 × 100,000 generated integers | 34.82 ms | 41.71 ms | 23.99 ms | 0.8× | 1.5× | Rust |
| stack | 1,000,000 push + pop | 10.57 ms | 15.06 ms | 9.37 ms | 0.7× | 1.1× | Rust |
| queue | 1,000,000 enqueue + dequeue | 10.61 ms | 15.25 ms | 10.29 ms | 0.7× | 1.0× | Rust |
| min-heap | 500,000 insert + remove-min | 51.40 ms | 61.44 ms | 33.44 ms | 0.8× | 1.5× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 34.02 ms | 27.01 ms | 24.23 ms | 1.3× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 89.18 ms | 64.03 ms | 27.19 ms | 1.4× | 3.3× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 41.49 ms | 45.07 ms | 39.03 ms | 0.9× | 1.1× | Rust |
| frequency-map | 1,000,000 integers; 4,096-key histogram | 129.14 ms | 14.71 ms | 22.48 ms | 8.8× | 5.7× | Go |
| unique-set | 1,000,000 integers; distinct-value count | 68.21 ms | 17.43 ms | 22.47 ms | 3.9× | 3.0× | Go |
| rune-frequency | 450,000 Unicode scalars; 12-key histogram | 67.75 ms | 6.91 ms | 6.81 ms | 9.8× | 9.9× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 50.39–61.70 ms | 29.54–35.10 ms | 28.53–33.56 ms |
| heap-sort | 32.37–38.85 ms | 39.02–45.78 ms | 22.41–26.26 ms |
| stack | 9.38–12.13 ms | 14.22–20.47 ms | 8.72–23.94 ms |
| queue | 9.66–11.55 ms | 14.34–20.73 ms | 8.59–11.99 ms |
| min-heap | 43.61–56.21 ms | 54.02–67.06 ms | 30.30–37.33 ms |
| dsu | 29.95–36.87 ms | 24.55–29.70 ms | 21.86–26.89 ms |
| bfs | 78.16–93.19 ms | 59.44–69.02 ms | 23.99–31.89 ms |
| dijkstra | 38.76–45.63 ms | 41.80–50.88 ms | 37.10–44.32 ms |
| frequency-map | 121.25–157.72 ms | 14.16–17.67 ms | 13.83–101.39 ms |
| unique-set | 62.72–78.78 ms | 16.49–21.48 ms | 19.23–25.14 ms |
| rune-frequency | 62.25–89.91 ms | 5.85–12.44 ms | 6.05–8.43 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- Every participant calls reusable package-owned algorithm code.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  absence representation follows each host language without changing timed valid inputs.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.9.6`
- marimay: `Marimay compiler 0.1.0-alpha.1`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
