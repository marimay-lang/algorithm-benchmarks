# Latest algorithm benchmark

Generated: `2026-08-21T19:42:02+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Ruda compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/ruda`.

Ruda source revision: `ae039188fa22b05a119a4dc5464f2a7f91d5deed`.

Algorithm corpus revision: `ed4a220aa1b88c2eb30b494bf33470a73762a12c`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 6978.96 ms | 41.76 ms | 39.98 ms | 167.1× | 174.5× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1998.88 ms | 51.74 ms | 44.05 ms | 38.6× | 45.4× | Rust |
| stack | 1,000,000 push + pop | 512.11 ms | 14.44 ms | 8.22 ms | 35.5× | 62.3× | Rust |
| queue | 1,000,000 enqueue + dequeue | 583.25 ms | 14.75 ms | 7.91 ms | 39.5× | 73.7× | Rust |
| min-heap | 500,000 insert + remove-min | 3734.37 ms | 74.08 ms | 56.42 ms | 50.4× | 66.2× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 3148.70 ms | 46.72 ms | 38.43 ms | 67.4× | 81.9× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 4547.90 ms | 111.17 ms | 47.08 ms | 40.9× | 96.6× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 1708.84 ms | 67.72 ms | 38.75 ms | 25.2× | 44.1× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 6889.22–7042.58 ms | 40.80–44.16 ms | 39.18–40.87 ms |
| heap-sort | 1987.80–2031.59 ms | 51.09–53.08 ms | 43.38–48.34 ms |
| stack | 507.27–516.12 ms | 13.79–15.69 ms | 7.78–8.44 ms |
| queue | 581.25–598.24 ms | 13.60–19.35 ms | 7.56–8.74 ms |
| min-heap | 3692.40–3801.58 ms | 72.04–78.61 ms | 55.84–58.09 ms |
| dsu | 3135.13–3225.21 ms | 45.92–48.25 ms | 37.49–38.87 ms |
| bfs | 4498.69–4592.82 ms | 102.24–129.74 ms | 46.65–51.75 ms |
| dijkstra | 1699.26–1728.77 ms | 67.04–68.77 ms | 38.10–40.31 ms |

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
