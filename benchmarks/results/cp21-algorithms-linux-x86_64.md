# Latest algorithm benchmark

Generated: `2026-08-22T06:10:31+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Ruda compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/ruda`.

Ruda source revision: `1b4a8b7cab70d5967440cb01854bd174078d0723`.

Algorithm corpus revision: `e74bd93b89b13b8aebd537d40326d7630f5ed461`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 7012.84 ms | 47.41 ms | 47.17 ms | 147.9× | 148.7× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1939.70 ms | 60.29 ms | 51.98 ms | 32.2× | 37.3× | Rust |
| stack | 1,000,000 push + pop | 605.67 ms | 19.76 ms | 10.44 ms | 30.6× | 58.0× | Rust |
| queue | 1,000,000 enqueue + dequeue | 718.82 ms | 26.64 ms | 9.10 ms | 27.0× | 79.0× | Rust |
| min-heap | 500,000 insert + remove-min | 3901.06 ms | 90.74 ms | 67.88 ms | 43.0× | 57.5× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 3910.54 ms | 53.52 ms | 44.53 ms | 73.1× | 87.8× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 5552.15 ms | 139.34 ms | 54.33 ms | 39.8× | 102.2× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 2121.95 ms | 79.38 ms | 45.98 ms | 26.7× | 46.2× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 6902.36–7744.68 ms | 46.66–59.10 ms | 45.82–56.16 ms |
| heap-sort | 1916.05–2134.29 ms | 58.88–104.18 ms | 50.92–60.34 ms |
| stack | 592.05–763.07 ms | 16.05–41.39 ms | 8.94–23.74 ms |
| queue | 707.95–807.90 ms | 15.88–48.54 ms | 8.67–15.22 ms |
| min-heap | 3846.68–4423.92 ms | 84.52–144.84 ms | 64.78–80.85 ms |
| dsu | 3743.77–4313.75 ms | 52.46–67.72 ms | 43.92–50.42 ms |
| bfs | 5183.21–5928.63 ms | 124.38–209.58 ms | 52.32–61.90 ms |
| dijkstra | 2053.57–2470.88 ms | 74.51–92.25 ms | 42.89–54.21 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- All three languages call reusable sorting, structures, and graph packages.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  Ruda and Rust model absence with Option while Go returns a value/bool pair.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.12.3`
- ruda: `Ruda compiler 0.0.0-dev`
- go: `go version go1.26.6 linux/amd64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
