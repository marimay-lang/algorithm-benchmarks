# Latest algorithm benchmark

Generated: `2026-08-21T22:47:55+07:00`

Host: `macOS-26.3.1-arm64-arm-64bit`; CPU: `Apple M2`.

Marimay compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/mmay`.

Marimay source revision: `bf8edd83e85cc2ed9c84791a2ea8cf0fe07146ae`.

Algorithm corpus revision: `033f17e9225d5760d40181ce13903bcda4decba3`.

Equivalence manifest: `benchmarks/equivalence.json` (`bf2f251de2d91e22d6696a50aa83babe9d1497139a305c4e1770e09c1f2f7e9b`).

Samples: 1 measured after 0 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 4271.70 ms | 430.02 ms | 298.74 ms | 9.9× | 14.3× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1258.78 ms | 41.13 ms | 21.97 ms | 30.6× | 57.3× | Rust |
| stack | 1,000,000 push + pop | 691.63 ms | 15.99 ms | 9.15 ms | 43.3× | 75.6× | Rust |
| queue | 1,000,000 enqueue + dequeue | 724.84 ms | 15.32 ms | 9.11 ms | 47.3× | 79.6× | Rust |
| min-heap | 500,000 insert + remove-min | 2143.32 ms | 54.51 ms | 30.09 ms | 39.3× | 71.2× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 2217.17 ms | 24.79 ms | 21.70 ms | 89.4× | 102.2× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 2746.55 ms | 62.04 ms | 24.40 ms | 44.3× | 112.6× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 1169.74 ms | 42.21 ms | 39.37 ms | 27.7× | 29.7× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 4271.70–4271.70 ms | 430.02–430.02 ms | 298.74–298.74 ms |
| heap-sort | 1258.78–1258.78 ms | 41.13–41.13 ms | 21.97–21.97 ms |
| stack | 691.63–691.63 ms | 15.99–15.99 ms | 9.15–9.15 ms |
| queue | 724.84–724.84 ms | 15.32–15.32 ms | 9.11–9.11 ms |
| min-heap | 2143.32–2143.32 ms | 54.51–54.51 ms | 30.09–30.09 ms |
| dsu | 2217.17–2217.17 ms | 24.79–24.79 ms | 21.70–21.70 ms |
| bfs | 2746.55–2746.55 ms | 62.04–62.04 ms | 24.40–24.40 ms |
| dijkstra | 1169.74–1169.74 ms | 42.21–42.21 ms | 39.37–39.37 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- All three languages call reusable sorting, structures, and graph packages.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  Marimay and Rust model absence with Option while Go returns a value/bool pair.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- Marimay: `Marimay compiler 0.0.0-dev`
- Go: `go version go1.26.4 darwin/arm64`
- Rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
