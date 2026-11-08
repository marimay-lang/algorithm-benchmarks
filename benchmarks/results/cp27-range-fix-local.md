# Latest algorithm benchmark

Generated: `2026-08-22T17:33:05+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Ruda compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/ruda`.

Ruda source revision: `17b7a1f1dcffd17659d84244c5f9981cdba867ea`.

Algorithm corpus revision: `1e7dbf794b57eb43d27dec401b066ffa8771d978`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Fastest |
|---|---|---:|---:|
| insertion | 50 × 2,500 generated integers | 2909.26 ms | Ruda |
| heap-sort | 5 × 100,000 generated integers | 729.28 ms | Ruda |
| stack | 1,000,000 push + pop | 400.65 ms | Ruda |
| queue | 1,000,000 enqueue + dequeue | 422.59 ms | Ruda |
| min-heap | 500,000 insert + remove-min | 1532.93 ms | Ruda |
| dsu | 100,000 nodes; 5,000,000 unions | 1698.10 ms | Ruda |
| bfs | 300 × 20,000 nodes, degree 4 | 2223.78 ms | Ruda |
| dijkstra | 80 × 800 nodes, O(V²) | 673.89 ms | Ruda |

## Range (min–max)

| Algorithm | Ruda |
|---|---:|
| insertion | 2907.54–2917.46 ms |
| heap-sort | 727.71–736.89 ms |
| stack | 396.32–408.93 ms |
| queue | 417.46–429.79 ms |
| min-heap | 1530.28–1540.03 ms |
| dsu | 1694.04–1825.91 ms |
| bfs | 2220.55–2336.88 ms |
| dijkstra | 672.44–682.59 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- All three languages call reusable sorting, structures, and graph packages.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  Ruda and Rust model absence with Option while Go returns a value/bool pair.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.9.6`
- ruda: `Ruda compiler 0.0.0-dev`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
