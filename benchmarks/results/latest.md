# Latest algorithm benchmark

Generated: `2026-09-06T22:26:08+07:00`

Host: `Darwin 25.6.0 arm64`; CPU: `Apple M2`.

Marimay compiler executable: `/path/to/Marimay/marimay/build/release/mmay`.

Marimay source revision: `52e5852616d2deb0694c4bfeeb469ae2e31e4599`.

Algorithm corpus revision: `3eda6055ff56be328c775c79d4a26ca412af66fb`.

Equivalence manifest: `benchmarks/equivalence.json` (`64ddc892dcac9a30a9e4b86aa669d1dff5a12aea65c3f353e180958f23a8c27a`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 50.91 ms | 29.17 ms | 28.72 ms | 1.7× | 1.8× | Rust |
| heap-sort | 5 × 100,000 generated integers | 32.23 ms | 39.14 ms | 22.01 ms | 0.8× | 1.5× | Rust |
| stack | 1,000,000 push + pop | 9.83 ms | 14.99 ms | 9.00 ms | 0.7× | 1.1× | Rust |
| queue | 1,000,000 enqueue + dequeue | 10.26 ms | 14.99 ms | 9.06 ms | 0.7× | 1.1× | Rust |
| min-heap | 500,000 insert + remove-min | 43.19 ms | 54.00 ms | 30.43 ms | 0.8× | 1.4× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 29.78 ms | 24.62 ms | 21.97 ms | 1.2× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 79.97 ms | 62.99 ms | 24.02 ms | 1.3× | 3.3× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 38.69 ms | 42.30 ms | 36.93 ms | 0.9× | 1.0× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 46.12–53.53 ms | 28.76–30.94 ms | 28.00–32.45 ms |
| heap-sort | 31.78–33.89 ms | 38.16–40.00 ms | 21.59–23.16 ms |
| stack | 9.51–13.82 ms | 14.56–17.00 ms | 8.79–11.52 ms |
| queue | 9.60–15.13 ms | 13.93–18.30 ms | 8.62–10.89 ms |
| min-heap | 41.84–44.66 ms | 52.81–60.96 ms | 29.57–32.61 ms |
| dsu | 29.41–32.34 ms | 24.18–26.54 ms | 21.39–25.80 ms |
| bfs | 77.95–83.85 ms | 60.59–65.29 ms | 23.15–28.48 ms |
| dijkstra | 38.36–40.84 ms | 40.62–45.27 ms | 36.55–38.65 ms |

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
