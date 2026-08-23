# Latest algorithm benchmark

Generated: `2026-08-23T05:03:40+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Marimay compiler executable: `/workspace/Marimay/algorithm-benchmarks/marimay/build/release/mmay`.

Marimay source revision: `95b74754403341e8306207a4f74e42010045a33a`.

Algorithm corpus revision: `0e998ccd27f7009f0efde490d95bbcdcb57be46b`.

Equivalence manifest: `benchmarks/equivalence.json` (`bf2f251de2d91e22d6696a50aa83babe9d1497139a305c4e1770e09c1f2f7e9b`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 70.70 ms | 49.01 ms | 46.52 ms | 1.4× | 1.5× | Rust |
| heap-sort | 5 × 100,000 generated integers | 90.90 ms | 59.77 ms | 51.35 ms | 1.5× | 1.8× | Rust |
| stack | 1,000,000 push + pop | 30.02 ms | 17.98 ms | 9.21 ms | 1.7× | 3.3× | Rust |
| queue | 1,000,000 enqueue + dequeue | 31.18 ms | 18.42 ms | 9.09 ms | 1.7× | 3.4× | Rust |
| min-heap | 500,000 insert + remove-min | 133.05 ms | 87.27 ms | 65.85 ms | 1.5× | 2.0× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 64.84 ms | 54.42 ms | 44.96 ms | 1.2× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 131.08 ms | 144.79 ms | 55.00 ms | 0.9× | 2.4× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 90.31 ms | 79.20 ms | 46.01 ms | 1.1× | 2.0× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 69.89–78.78 ms | 47.52–52.03 ms | 45.68–52.06 ms |
| heap-sort | 89.82–100.30 ms | 59.04–70.69 ms | 50.49–55.45 ms |
| stack | 29.36–39.46 ms | 15.96–28.85 ms | 8.93–10.55 ms |
| queue | 30.58–43.25 ms | 16.48–28.84 ms | 8.60–11.19 ms |
| min-heap | 130.83–143.37 ms | 83.43–91.68 ms | 64.49–67.60 ms |
| dsu | 63.59–68.01 ms | 53.19–59.09 ms | 43.90–46.97 ms |
| bfs | 128.70–143.29 ms | 133.81–170.21 ms | 53.89–57.42 ms |
| dijkstra | 89.42–97.90 ms | 78.40–88.22 ms | 45.57–46.95 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- Every participant calls reusable sorting, structures, and graph code.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  absence representation follows each host language without changing timed valid inputs.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.12.3`
- marimay: `Marimay compiler 0.0.0-dev`
- go: `go version go1.26.6 linux/amd64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
