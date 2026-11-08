# Latest algorithm benchmark

Generated: `2026-09-06T22:26:49+07:00`

Host: `Darwin 25.6.0 arm64`; CPU: `Apple M2`.

Marimay compiler executable: `/path/to/Marimay/marimay/build/release/mmay`.

Marimay source revision: `52e5852616d2deb0694c4bfeeb469ae2e31e4599`.

Algorithm corpus revision: `3eda6055ff56be328c775c79d4a26ca412af66fb`.

Equivalence manifest: `benchmarks/equivalence.json` (`64ddc892dcac9a30a9e4b86aa669d1dff5a12aea65c3f353e180958f23a8c27a`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 51.61 ms | 30.00 ms | 31.35 ms | 1.7× | 1.6× | Go |
| heap-sort | 5 × 100,000 generated integers | 34.71 ms | 41.57 ms | 23.22 ms | 0.8× | 1.5× | Rust |
| stack | 1,000,000 push + pop | 11.52 ms | 16.01 ms | 10.08 ms | 0.7× | 1.1× | Rust |
| queue | 1,000,000 enqueue + dequeue | 10.67 ms | 16.97 ms | 9.17 ms | 0.6× | 1.2× | Rust |
| min-heap | 500,000 insert + remove-min | 44.75 ms | 57.75 ms | 31.21 ms | 0.8× | 1.4× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 30.47 ms | 24.80 ms | 21.93 ms | 1.2× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 82.02 ms | 64.07 ms | 24.29 ms | 1.3× | 3.4× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 40.32 ms | 42.10 ms | 37.84 ms | 1.0× | 1.1× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 48.52–316.94 ms | 28.74–39.27 ms | 28.17–41.68 ms |
| heap-sort | 31.87–297.34 ms | 38.92–65.33 ms | 21.87–53.94 ms |
| stack | 9.44–264.64 ms | 14.43–21.59 ms | 8.74–11.46 ms |
| queue | 9.67–273.77 ms | 14.43–23.00 ms | 8.79–15.60 ms |
| min-heap | 43.34–398.65 ms | 54.03–150.37 ms | 29.34–300.82 ms |
| dsu | 29.50–313.19 ms | 24.05–56.66 ms | 21.45–26.69 ms |
| bfs | 78.61–373.52 ms | 61.00–80.72 ms | 23.91–33.51 ms |
| dijkstra | 38.16–282.10 ms | 40.98–63.53 ms | 36.70–55.42 ms |

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
