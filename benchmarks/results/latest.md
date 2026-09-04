# Latest algorithm benchmark

Generated: `2026-08-28T23:45:29+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Marimay compiler executable: `/path/to/Marimay/marimay/build/release/mmay`.

Marimay source revision: `e03bc771d5a79bc6ff210aa5d2b4f39e4ec74349`.

Algorithm corpus revision: `b5c0492eab752e6a05b572eee0b23416badafd24`.

Equivalence manifest: `benchmarks/equivalence.json` (`64ddc892dcac9a30a9e4b86aa669d1dff5a12aea65c3f353e180958f23a8c27a`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 51.25 ms | 29.29 ms | 28.59 ms | 1.7× | 1.8× | Rust |
| heap-sort | 5 × 100,000 generated integers | 33.07 ms | 39.40 ms | 22.37 ms | 0.8× | 1.5× | Rust |
| stack | 1,000,000 push + pop | 13.83 ms | 16.10 ms | 9.12 ms | 0.9× | 1.5× | Rust |
| queue | 1,000,000 enqueue + dequeue | 13.20 ms | 14.97 ms | 8.90 ms | 0.9× | 1.5× | Rust |
| min-heap | 500,000 insert + remove-min | 52.49 ms | 54.88 ms | 30.96 ms | 1.0× | 1.7× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 31.23 ms | 24.40 ms | 21.58 ms | 1.3× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 70.99 ms | 63.37 ms | 24.23 ms | 1.1× | 2.9× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 41.64 ms | 41.24 ms | 39.31 ms | 1.0× | 1.1× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 47.35–53.42 ms | 28.92–31.63 ms | 28.14–29.24 ms |
| heap-sort | 31.93–35.25 ms | 38.73–51.46 ms | 21.75–23.97 ms |
| stack | 12.41–16.89 ms | 14.03–29.12 ms | 8.56–18.15 ms |
| queue | 12.78–14.35 ms | 13.53–16.25 ms | 8.71–9.92 ms |
| min-heap | 50.66–57.43 ms | 52.54–59.51 ms | 29.77–37.54 ms |
| dsu | 30.63–33.39 ms | 24.11–29.18 ms | 21.37–23.46 ms |
| bfs | 69.63–78.52 ms | 62.15–64.40 ms | 23.45–32.88 ms |
| dijkstra | 40.82–42.50 ms | 40.44–54.02 ms | 38.80–131.75 ms |

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
