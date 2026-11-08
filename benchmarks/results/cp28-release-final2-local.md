# Latest algorithm benchmark

Generated: `2026-08-22T18:53:45+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Ruda compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/ruda`.

Ruda source revision: `17b7a1f1dcffd17659d84244c5f9981cdba867ea`.

Algorithm corpus revision: `1e7dbf794b57eb43d27dec401b066ffa8771d978`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 299.83 ms | 28.87 ms | 28.16 ms | 10.4× | 10.6× | Rust |
| heap-sort | 5 × 100,000 generated integers | 129.41 ms | 38.98 ms | 21.71 ms | 3.3× | 6.0× | Rust |
| stack | 1,000,000 push + pop | 267.91 ms | 14.65 ms | 8.92 ms | 18.3× | 30.0× | Rust |
| queue | 1,000,000 enqueue + dequeue | 264.93 ms | 14.90 ms | 9.01 ms | 17.8× | 29.4× | Rust |
| min-heap | 500,000 insert + remove-min | 400.78 ms | 53.29 ms | 29.33 ms | 7.5× | 13.7× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 481.45 ms | 24.60 ms | 21.82 ms | 19.6× | 22.1× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 985.33 ms | 62.96 ms | 23.76 ms | 15.7× | 41.5× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 186.85 ms | 40.66 ms | 38.96 ms | 4.6× | 4.8× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 299.34–301.65 ms | 28.63–29.41 ms | 27.87–28.91 ms |
| heap-sort | 127.92–129.88 ms | 38.27–39.19 ms | 21.55–21.96 ms |
| stack | 264.25–275.62 ms | 14.56–15.76 ms | 8.68–10.54 ms |
| queue | 261.61–266.24 ms | 14.33–15.48 ms | 8.77–9.20 ms |
| min-heap | 397.30–404.09 ms | 52.05–55.46 ms | 29.07–29.57 ms |
| dsu | 480.34–498.52 ms | 23.89–26.26 ms | 21.30–25.24 ms |
| bfs | 981.80–1024.59 ms | 59.94–64.44 ms | 23.49–24.32 ms |
| dijkstra | 186.06–212.99 ms | 40.39–42.73 ms | 38.53–39.50 ms |

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
