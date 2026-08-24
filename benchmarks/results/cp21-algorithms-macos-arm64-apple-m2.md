# Latest algorithm benchmark

Generated: `2026-08-21T23:58:14+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Marimay compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/mmay`.

Marimay source revision: `d6afbe792685ef12fe1ce9e6e053ad9758ddce8d`.

Algorithm corpus revision: `57ad442f62ee644c82bd48243913c55cf0d27dac`.

Equivalence manifest: `benchmarks/equivalence.json` (`64ddc892dcac9a30a9e4b86aa669d1dff5a12aea65c3f353e180958f23a8c27a`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 4003.60 ms | 29.56 ms | 28.82 ms | 135.4× | 138.9× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1007.91 ms | 39.51 ms | 22.50 ms | 25.5× | 44.8× | Rust |
| stack | 1,000,000 push + pop | 395.26 ms | 15.45 ms | 9.40 ms | 25.6× | 42.0× | Rust |
| queue | 1,000,000 enqueue + dequeue | 429.97 ms | 15.76 ms | 9.61 ms | 27.3× | 44.7× | Rust |
| min-heap | 500,000 insert + remove-min | 1896.28 ms | 54.69 ms | 30.55 ms | 34.7× | 62.1× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 1948.33 ms | 25.05 ms | 22.31 ms | 77.8× | 87.3× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 2488.14 ms | 62.84 ms | 24.81 ms | 39.6× | 100.3× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 885.37 ms | 41.70 ms | 39.44 ms | 21.2× | 22.4× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 3911.21–4399.91 ms | 28.97–69.71 ms | 28.35–29.91 ms |
| heap-sort | 985.13–1214.07 ms | 38.86–51.44 ms | 21.98–33.08 ms |
| stack | 386.82–409.86 ms | 14.32–16.37 ms | 8.96–10.85 ms |
| queue | 428.09–447.69 ms | 14.51–16.87 ms | 9.08–17.47 ms |
| min-heap | 1847.37–1976.73 ms | 54.05–57.93 ms | 30.28–32.72 ms |
| dsu | 1921.16–2095.53 ms | 24.49–26.81 ms | 21.64–23.86 ms |
| bfs | 2464.54–2717.68 ms | 61.36–104.91 ms | 23.77–53.36 ms |
| dijkstra | 883.06–996.17 ms | 41.00–43.98 ms | 39.06–41.38 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- All three languages call reusable sorting, structures, and graph packages.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  Marimay and Rust model absence with Option while Go returns a value/bool pair.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.9.6`
- marimay: `Marimay compiler 0.0.0-dev`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
