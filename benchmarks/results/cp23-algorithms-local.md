# Latest algorithm benchmark

Generated: `2026-08-23T00:56:17+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Ruda compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/ruda`.

Ruda source revision: `c17ae83ba16d021363cefb3c4fdb2e2138faab87`.

Algorithm corpus revision: `1588f070db936168bd10d8e8e4a0d5f7a5751c46`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 51.55 ms | 30.33 ms | 29.67 ms | 1.7× | 1.7× | Rust |
| heap-sort | 5 × 100,000 generated integers | 32.75 ms | 39.87 ms | 22.64 ms | 0.8× | 1.4× | Rust |
| stack | 1,000,000 push + pop | 12.78 ms | 15.33 ms | 9.27 ms | 0.8× | 1.4× | Rust |
| queue | 1,000,000 enqueue + dequeue | 13.07 ms | 15.40 ms | 9.29 ms | 0.8× | 1.4× | Rust |
| min-heap | 500,000 insert + remove-min | 56.94 ms | 56.95 ms | 32.24 ms | 1.0× | 1.8× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 32.56 ms | 25.42 ms | 22.72 ms | 1.3× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 55.43 ms | 61.26 ms | 25.33 ms | 0.9× | 2.2× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 42.85 ms | 42.96 ms | 40.97 ms | 1.0× | 1.0× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 50.63–54.51 ms | 29.37–32.21 ms | 28.48–30.83 ms |
| heap-sort | 32.19–35.99 ms | 38.79–41.73 ms | 21.82–24.76 ms |
| stack | 12.20–14.12 ms | 14.84–18.53 ms | 8.83–10.68 ms |
| queue | 12.56–14.63 ms | 14.00–17.19 ms | 8.64–10.43 ms |
| min-heap | 52.38–60.25 ms | 54.10–60.13 ms | 30.68–35.92 ms |
| dsu | 31.46–33.36 ms | 24.45–26.31 ms | 21.60–26.07 ms |
| bfs | 52.51–64.23 ms | 58.61–65.62 ms | 24.49–27.96 ms |
| dijkstra | 41.53–44.97 ms | 41.25–45.07 ms | 39.11–42.70 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- Every participant calls reusable sorting, structures, and graph code.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  absence representation follows each host language without changing timed valid inputs.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.9.6`
- ruda: `Ruda compiler 0.0.0-dev`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
