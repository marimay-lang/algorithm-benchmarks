# Latest algorithm benchmark

Generated: `2026-08-22T12:55:39+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Ruda compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/ruda`.

Ruda source revision: `17b7a1f1dcffd17659d84244c5f9981cdba867ea`.

Algorithm corpus revision: `1588f070db936168bd10d8e8e4a0d5f7a5751c46`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 4526.35 ms | 41.56 ms | 40.45 ms | 108.9× | 111.9× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1193.25 ms | 52.01 ms | 43.95 ms | 22.9× | 27.2× | Rust |
| stack | 1,000,000 push + pop | 502.08 ms | 14.57 ms | 8.18 ms | 34.5× | 61.4× | Rust |
| queue | 1,000,000 enqueue + dequeue | 567.42 ms | 14.90 ms | 7.76 ms | 38.1× | 73.1× | Rust |
| min-heap | 500,000 insert + remove-min | 2599.11 ms | 74.75 ms | 56.62 ms | 34.8× | 45.9× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 2640.37 ms | 46.98 ms | 38.14 ms | 56.2× | 69.2× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 3763.75 ms | 105.94 ms | 47.34 ms | 35.5× | 79.5× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 1064.06 ms | 67.96 ms | 39.40 ms | 15.7× | 27.0× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 4495.11–4554.51 ms | 40.75–42.55 ms | 39.28–44.19 ms |
| heap-sort | 1182.39–1209.07 ms | 50.72–54.19 ms | 43.35–45.84 ms |
| stack | 498.61–517.98 ms | 13.65–16.68 ms | 7.89–8.43 ms |
| queue | 561.99–581.32 ms | 13.75–16.23 ms | 7.43–8.14 ms |
| min-heap | 2579.76–2642.34 ms | 72.43–76.38 ms | 55.93–60.60 ms |
| dsu | 2598.60–2657.95 ms | 46.22–48.19 ms | 37.10–39.56 ms |
| bfs | 3732.68–3843.07 ms | 102.64–112.33 ms | 45.87–51.69 ms |
| dijkstra | 1056.10–1081.70 ms | 66.94–70.61 ms | 38.33–40.43 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- Every participant calls reusable sorting, structures, and graph code.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  absence representation follows each host language without changing timed valid inputs.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.12.3`
- ruda: `Ruda compiler 0.0.0-dev`
- go: `go version go1.26.6 linux/amd64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
