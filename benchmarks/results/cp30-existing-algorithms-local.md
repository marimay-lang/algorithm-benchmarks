# Latest algorithm benchmark

Generated: `2026-08-23T23:37:15+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Marimay compiler executable: `/path/to/Marimay/marimay/build/release/mmay`.

Marimay source revision: `56fb0870b976c7ec1e7b2f43bb8bf1985e2ad4f3`.

Algorithm corpus revision: `0e998ccd27f7009f0efde490d95bbcdcb57be46b`.

Equivalence manifest: `benchmarks/equivalence.json` (`bf2f251de2d91e22d6696a50aa83babe9d1497139a305c4e1770e09c1f2f7e9b`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 51.23 ms | 29.82 ms | 28.88 ms | 1.7× | 1.8× | Rust |
| heap-sort | 5 × 100,000 generated integers | 32.57 ms | 39.84 ms | 22.72 ms | 0.8× | 1.4× | Rust |
| stack | 1,000,000 push + pop | 12.75 ms | 15.03 ms | 9.20 ms | 0.8× | 1.4× | Rust |
| queue | 1,000,000 enqueue + dequeue | 12.90 ms | 15.22 ms | 9.23 ms | 0.8× | 1.4× | Rust |
| min-heap | 500,000 insert + remove-min | 54.24 ms | 55.05 ms | 30.77 ms | 1.0× | 1.8× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 31.74 ms | 24.76 ms | 22.24 ms | 1.3× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 53.11 ms | 63.97 ms | 24.73 ms | 0.8× | 2.1× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 42.03 ms | 41.79 ms | 40.00 ms | 1.0× | 1.1× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 48.64–52.76 ms | 28.87–30.71 ms | 28.47–29.63 ms |
| heap-sort | 31.93–33.42 ms | 38.79–40.73 ms | 21.98–23.86 ms |
| stack | 12.15–14.18 ms | 14.41–58.86 ms | 8.83–21.74 ms |
| queue | 12.71–18.88 ms | 14.39–15.93 ms | 8.79–10.07 ms |
| min-heap | 52.38–55.84 ms | 54.03–57.56 ms | 29.91–34.09 ms |
| dsu | 31.08–33.35 ms | 24.01–25.87 ms | 21.81–23.59 ms |
| bfs | 52.05–55.75 ms | 61.10–66.10 ms | 23.90–25.92 ms |
| dijkstra | 41.33–42.91 ms | 41.31–43.93 ms | 39.42–41.77 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- Every participant calls reusable sorting, structures, and graph code.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  absence representation follows each host language without changing timed valid inputs.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.9.6`
- marimay: `Marimay compiler 0.1.0-alpha.1`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
