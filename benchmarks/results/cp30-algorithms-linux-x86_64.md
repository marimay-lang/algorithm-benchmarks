# Latest algorithm benchmark

Generated: `2026-08-24T18:50:34+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Marimay compiler executable: `/workspace/Marimay/algorithm-benchmarks/marimay/build/release/mmay`.

Marimay source revision: `cd31289ddb34d4ecdeef619acc0f7527ba691db6`.

Algorithm corpus revision: `b5c0492eab752e6a05b572eee0b23416badafd24`.

Equivalence manifest: `benchmarks/equivalence.json` (`64ddc892dcac9a30a9e4b86aa669d1dff5a12aea65c3f353e180958f23a8c27a`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 65.83 ms | 44.98 ms | 43.39 ms | 1.5× | 1.5× | Rust |
| heap-sort | 5 × 100,000 generated integers | 84.88 ms | 56.31 ms | 47.63 ms | 1.5× | 1.8× | Rust |
| stack | 1,000,000 push + pop | 27.65 ms | 15.81 ms | 8.49 ms | 1.7× | 3.3× | Rust |
| queue | 1,000,000 enqueue + dequeue | 29.80 ms | 16.53 ms | 8.33 ms | 1.8× | 3.6× | Rust |
| min-heap | 500,000 insert + remove-min | 117.72 ms | 79.85 ms | 61.57 ms | 1.5× | 1.9× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 60.37 ms | 50.13 ms | 41.27 ms | 1.2× | 1.5× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 139.96 ms | 121.03 ms | 50.59 ms | 1.2× | 2.8× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 78.49 ms | 74.14 ms | 42.37 ms | 1.1× | 1.9× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 65.09–67.55 ms | 43.69–48.19 ms | 42.87–44.90 ms |
| heap-sort | 83.33–86.23 ms | 55.23–59.30 ms | 46.99–48.50 ms |
| stack | 27.09–31.14 ms | 14.13–21.12 ms | 8.19–10.00 ms |
| queue | 29.39–34.89 ms | 14.69–17.92 ms | 7.94–9.17 ms |
| min-heap | 116.15–125.44 ms | 78.07–81.40 ms | 60.14–64.71 ms |
| dsu | 60.03–62.20 ms | 49.70–52.84 ms | 40.15–45.47 ms |
| bfs | 138.18–146.63 ms | 113.60–142.93 ms | 49.39–52.32 ms |
| dijkstra | 77.92–79.77 ms | 73.31–76.42 ms | 42.18–49.85 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- Every participant calls reusable sorting, structures, and graph code.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  absence representation follows each host language without changing timed valid inputs.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.12.3`
- marimay: `Marimay compiler 0.1.0-alpha.1`
- go: `go version go1.26.6 linux/amd64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
