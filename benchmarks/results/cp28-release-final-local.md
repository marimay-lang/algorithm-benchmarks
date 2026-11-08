# Latest algorithm benchmark

Generated: `2026-08-22T18:51:03+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Ruda compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/ruda`.

Ruda source revision: `17b7a1f1dcffd17659d84244c5f9981cdba867ea`.

Algorithm corpus revision: `1e7dbf794b57eb43d27dec401b066ffa8771d978`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 301.68 ms | 29.41 ms | 28.62 ms | 10.3× | 10.5× | Rust |
| heap-sort | 5 × 100,000 generated integers | 130.38 ms | 39.66 ms | 22.22 ms | 3.3× | 5.9× | Rust |
| stack | 1,000,000 push + pop | 273.96 ms | 15.49 ms | 9.38 ms | 17.7× | 29.2× | Rust |
| queue | 1,000,000 enqueue + dequeue | 272.20 ms | 15.69 ms | 9.48 ms | 17.4× | 28.7× | Rust |
| min-heap | 500,000 insert + remove-min | 481.47 ms | 54.15 ms | 30.10 ms | 8.9× | 16.0× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 555.35 ms | 24.98 ms | 22.06 ms | 22.2× | 25.2× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 1000.07 ms | 63.10 ms | 24.40 ms | 15.8× | 41.0× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 188.64 ms | 41.47 ms | 39.53 ms | 4.5× | 4.8× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 300.85–302.91 ms | 28.99–29.86 ms | 28.20–29.05 ms |
| heap-sort | 129.72–131.68 ms | 38.77–41.25 ms | 21.93–22.43 ms |
| stack | 272.79–282.85 ms | 14.60–15.93 ms | 8.93–9.60 ms |
| queue | 270.34–277.81 ms | 14.75–16.88 ms | 9.00–10.14 ms |
| min-heap | 478.61–492.82 ms | 53.44–54.80 ms | 29.76–32.23 ms |
| dsu | 551.36–559.60 ms | 24.10–27.24 ms | 21.56–22.46 ms |
| bfs | 993.75–1123.03 ms | 61.89–64.65 ms | 23.74–24.81 ms |
| dijkstra | 187.60–189.55 ms | 40.78–42.00 ms | 39.11–40.03 ms |

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
