# Expanded local algorithm benchmark

Generated: `2026-09-09T15:15:13+07:00`

Host: `Darwin 25.6.0 arm64`; CPU: `Apple M2`.

Marimay compiler executable: `/path/to/Marimay/marimay/build/release/mmay`.

Marimay source revision: `8ac216c345063afe1610c82d5b3a7aa05bfefd96`.

Algorithm corpus revision: `3eda6055ff56be328c775c79d4a26ca412af66fb`.

Equivalence manifest: `benchmarks/equivalence.json` (`64ddc892dcac9a30a9e4b86aa669d1dff5a12aea65c3f353e180958f23a8c27a`).

Expanded workload manifest: `benchmarks/expanded_workloads.json` (`ef6e688152b4bfe2906dd7ef22f285fc8a94d900d90c8518b0698a4da1aa1188`).

This extended matrix is local-only and is excluded from Tier 1 baselines.

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 52.40 ms | 28.86 ms | 28.03 ms | 1.8× | 1.9× | Rust |
| heap-sort | 5 × 100,000 generated integers | 31.66 ms | 38.49 ms | 21.66 ms | 0.8× | 1.5× | Rust |
| stack | 1,000,000 push + pop | 9.41 ms | 14.34 ms | 8.56 ms | 0.7× | 1.1× | Rust |
| queue | 1,000,000 enqueue + dequeue | 9.49 ms | 14.31 ms | 8.83 ms | 0.7× | 1.1× | Rust |
| min-heap | 500,000 insert + remove-min | 43.30 ms | 52.96 ms | 28.72 ms | 0.8× | 1.5× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 29.27 ms | 23.96 ms | 21.33 ms | 1.2× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 61.75 ms | 62.58 ms | 23.45 ms | 1.0× | 2.6× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 38.42 ms | 40.70 ms | 38.82 ms | 0.9× | 1.0× | Marimay |
| frequency-map | 1,000,000 integers; 4,096-key histogram | 32.50 ms | 13.67 ms | 24.53 ms | 2.4× | 1.3× | Go |
| unique-set | 1,000,000 integers; distinct-value count | 26.71 ms | 16.16 ms | 18.39 ms | 1.7× | 1.5× | Go |
| rune-frequency | 450,000 Unicode scalars; 12-key histogram | 22.10 ms | 6.02 ms | 5.85 ms | 3.7× | 3.8× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 49.01–53.67 ms | 28.57–31.38 ms | 27.80–28.82 ms |
| heap-sort | 31.49–125.53 ms | 38.25–38.91 ms | 21.62–22.05 ms |
| stack | 9.23–9.91 ms | 13.91–14.81 ms | 8.46–8.69 ms |
| queue | 9.29–9.64 ms | 13.96–14.91 ms | 8.58–9.04 ms |
| min-heap | 43.11–45.81 ms | 52.26–53.75 ms | 28.22–31.35 ms |
| dsu | 29.16–30.80 ms | 23.79–24.67 ms | 21.26–22.70 ms |
| bfs | 61.23–68.61 ms | 61.06–64.76 ms | 23.10–25.62 ms |
| dijkstra | 38.07–38.64 ms | 40.23–42.47 ms | 38.75–39.97 ms |
| frequency-map | 32.27–32.96 ms | 13.47–14.37 ms | 13.31–25.00 ms |
| unique-set | 26.49–27.37 ms | 15.52–17.16 ms | 18.16–19.91 ms |
| rune-frequency | 21.96–25.30 ms | 5.31–6.36 ms | 5.65–7.08 ms |

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
