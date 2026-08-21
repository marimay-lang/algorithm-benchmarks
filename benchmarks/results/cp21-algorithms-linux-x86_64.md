# Latest algorithm benchmark

Generated: `2026-08-21T19:31:17+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Ruda compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/ruda`.

Ruda source revision: `ae039188fa22b05a119a4dc5464f2a7f91d5deed`.

Algorithm corpus revision: `22be069a00c563f3261d0dd79759b6a7eb48dd2d`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 6999.18 ms | 41.49 ms | 40.95 ms | 168.7× | 170.9× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1790.07 ms | 52.28 ms | 44.48 ms | 34.2× | 40.2× | Rust |
| stack | 1,000,000 push + pop | 522.08 ms | 14.48 ms | 8.39 ms | 36.1× | 62.2× | Rust |
| queue | 1,000,000 enqueue + dequeue | 588.69 ms | 14.78 ms | 7.93 ms | 39.8× | 74.2× | Rust |
| min-heap | 500,000 insert + remove-min | 3760.09 ms | 74.55 ms | 56.62 ms | 50.4× | 66.4× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 3188.85 ms | 46.82 ms | 38.51 ms | 68.1× | 82.8× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 4541.52 ms | 105.83 ms | 47.08 ms | 42.9× | 96.5× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 1727.68 ms | 68.51 ms | 39.40 ms | 25.2× | 43.8× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 6930.73–7073.41 ms | 40.84–45.91 ms | 39.38–45.87 ms |
| heap-sort | 1766.23–1874.67 ms | 51.46–53.70 ms | 43.45–49.16 ms |
| stack | 517.99–542.16 ms | 13.61–17.51 ms | 7.77–8.62 ms |
| queue | 582.76–596.84 ms | 14.07–20.01 ms | 7.65–9.48 ms |
| min-heap | 3724.37–3794.16 ms | 71.91–78.69 ms | 55.34–64.72 ms |
| dsu | 3160.36–3218.79 ms | 46.06–50.40 ms | 37.66–39.27 ms |
| bfs | 4516.11–4624.31 ms | 102.69–116.98 ms | 45.90–48.49 ms |
| dijkstra | 1710.78–1753.43 ms | 67.12–74.19 ms | 38.63–40.13 ms |

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
