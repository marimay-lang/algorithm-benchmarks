# Latest algorithm benchmark

Generated: `2026-08-22T09:17:10+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Ruda compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/ruda`.

Ruda source revision: `17b7a1f1dcffd17659d84244c5f9981cdba867ea`.

Algorithm corpus revision: `1e7dbf794b57eb43d27dec401b066ffa8771d978`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 4526.34 ms | 41.62 ms | 40.19 ms | 108.8× | 112.6× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1195.16 ms | 52.38 ms | 43.99 ms | 22.8× | 27.2× | Rust |
| stack | 1,000,000 push + pop | 507.42 ms | 14.65 ms | 8.08 ms | 34.6× | 62.8× | Rust |
| queue | 1,000,000 enqueue + dequeue | 576.20 ms | 14.73 ms | 7.90 ms | 39.1× | 72.9× | Rust |
| min-heap | 500,000 insert + remove-min | 2597.00 ms | 75.20 ms | 56.47 ms | 34.5× | 46.0× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 2623.16 ms | 47.37 ms | 38.56 ms | 55.4× | 68.0× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 3756.04 ms | 106.62 ms | 47.26 ms | 35.2× | 79.5× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 1069.62 ms | 68.17 ms | 39.10 ms | 15.7× | 27.4× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 4499.80–4550.67 ms | 41.03–44.26 ms | 39.33–41.94 ms |
| heap-sort | 1189.70–1211.40 ms | 51.16–52.77 ms | 43.01–45.22 ms |
| stack | 498.38–525.27 ms | 13.19–18.18 ms | 7.89–9.16 ms |
| queue | 568.34–584.12 ms | 13.97–16.19 ms | 7.60–8.34 ms |
| min-heap | 2582.22–2608.48 ms | 72.52–78.79 ms | 55.30–57.67 ms |
| dsu | 2606.21–2657.82 ms | 46.44–50.39 ms | 37.16–44.54 ms |
| bfs | 3709.43–3834.19 ms | 101.30–113.49 ms | 45.56–49.19 ms |
| dijkstra | 1058.37–1079.40 ms | 67.43–69.93 ms | 38.23–42.81 ms |

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
