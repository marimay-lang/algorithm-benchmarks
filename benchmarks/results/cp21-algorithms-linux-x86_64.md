# Latest algorithm benchmark

Generated: `2026-08-22T05:20:51+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Marimay compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/mmay`.

Marimay source revision: `1d728451612f5ad4d6cfb78a5785b2e57605af26`.

Algorithm corpus revision: `c8da4676e0e80522d795a6b7fe551e93916c9fad`.

Equivalence manifest: `benchmarks/equivalence.json` (`64ddc892dcac9a30a9e4b86aa669d1dff5a12aea65c3f353e180958f23a8c27a`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 6038.62 ms | 41.84 ms | 39.91 ms | 144.3× | 151.3× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1650.28 ms | 52.11 ms | 44.15 ms | 31.7× | 37.4× | Rust |
| stack | 1,000,000 push + pop | 515.24 ms | 14.74 ms | 8.30 ms | 35.0× | 62.1× | Rust |
| queue | 1,000,000 enqueue + dequeue | 593.95 ms | 15.33 ms | 7.95 ms | 38.8× | 74.7× | Rust |
| min-heap | 500,000 insert + remove-min | 3292.64 ms | 75.10 ms | 57.12 ms | 43.8× | 57.6× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 3234.76 ms | 47.04 ms | 38.94 ms | 68.8× | 83.1× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 4479.39 ms | 107.75 ms | 47.69 ms | 41.6× | 93.9× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 1845.18 ms | 69.11 ms | 39.42 ms | 26.7× | 46.8× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 5971.71–6498.20 ms | 41.13–45.23 ms | 39.24–41.95 ms |
| heap-sort | 1635.99–1728.05 ms | 51.35–53.09 ms | 43.42–46.18 ms |
| stack | 507.45–526.66 ms | 13.74–17.41 ms | 7.93–9.19 ms |
| queue | 586.33–608.30 ms | 13.65–19.00 ms | 7.64–9.01 ms |
| min-heap | 3237.68–3355.25 ms | 72.95–79.02 ms | 55.62–65.55 ms |
| dsu | 3206.77–3358.04 ms | 46.45–51.66 ms | 37.46–41.97 ms |
| bfs | 4401.60–4990.60 ms | 102.42–112.70 ms | 46.20–49.35 ms |
| dijkstra | 1824.55–1948.19 ms | 66.92–72.10 ms | 38.76–41.42 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- All three languages call reusable sorting, structures, and graph packages.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  Marimay and Rust model absence with Option while Go returns a value/bool pair.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.12.3`
- marimay: `Marimay compiler 0.0.0-dev`
- go: `go version go1.26.6 linux/amd64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
