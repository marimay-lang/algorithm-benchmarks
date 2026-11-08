# Latest algorithm benchmark

Generated: `2026-08-22T18:13:01+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Ruda compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/ruda`.

Ruda source revision: `17b7a1f1dcffd17659d84244c5f9981cdba867ea`.

Algorithm corpus revision: `1e7dbf794b57eb43d27dec401b066ffa8771d978`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 301.69 ms | 29.34 ms | 28.45 ms | 10.3× | 10.6× | Rust |
| heap-sort | 5 × 100,000 generated integers | 130.13 ms | 39.56 ms | 22.13 ms | 3.3× | 5.9× | Rust |
| stack | 1,000,000 push + pop | 270.31 ms | 14.82 ms | 9.13 ms | 18.2× | 29.6× | Rust |
| queue | 1,000,000 enqueue + dequeue | 267.57 ms | 15.06 ms | 9.30 ms | 17.8× | 28.8× | Rust |
| min-heap | 500,000 insert + remove-min | 399.28 ms | 54.16 ms | 29.83 ms | 7.4× | 13.4× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 477.33 ms | 24.60 ms | 21.94 ms | 19.4× | 21.8× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 995.68 ms | 63.24 ms | 24.11 ms | 15.7× | 41.3× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 187.89 ms | 41.37 ms | 39.44 ms | 4.5× | 4.8× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 300.90–303.50 ms | 28.90–29.89 ms | 28.15–29.07 ms |
| heap-sort | 129.63–133.49 ms | 38.83–39.86 ms | 21.94–22.63 ms |
| stack | 267.79–271.89 ms | 14.29–15.41 ms | 8.91–9.42 ms |
| queue | 265.20–276.00 ms | 14.48–15.61 ms | 8.94–9.71 ms |
| min-heap | 394.09–513.05 ms | 53.33–55.04 ms | 29.69–31.80 ms |
| dsu | 476.41–487.95 ms | 24.07–25.23 ms | 21.70–22.12 ms |
| bfs | 992.78–1002.81 ms | 61.61–64.41 ms | 23.57–24.63 ms |
| dijkstra | 187.51–189.64 ms | 40.62–41.90 ms | 39.12–40.37 ms |

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
