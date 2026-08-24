# Latest algorithm benchmark

Generated: `2026-08-24T09:17:27+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Marimay compiler executable: `/workspace/Marimay/algorithm-benchmarks/marimay/build/release/mmay`.

Marimay source revision: `97cbc0e152bfbdc06a9806bafbf8515dd6ee17e3`.

Algorithm corpus revision: `4a0d56662e167a18f9b2ee8690af31fcd0ad958b`.

Equivalence manifest: `benchmarks/equivalence.json` (`bf2f251de2d91e22d6696a50aa83babe9d1497139a305c4e1770e09c1f2f7e9b`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 91.25 ms | 48.72 ms | 47.17 ms | 1.9× | 1.9× | Rust |
| heap-sort | 5 × 100,000 generated integers | 90.58 ms | 60.98 ms | 51.46 ms | 1.5× | 1.8× | Rust |
| stack | 1,000,000 push + pop | 30.48 ms | 19.03 ms | 9.64 ms | 1.6× | 3.2× | Rust |
| queue | 1,000,000 enqueue + dequeue | 32.01 ms | 22.54 ms | 9.70 ms | 1.4× | 3.3× | Rust |
| min-heap | 500,000 insert + remove-min | 131.54 ms | 86.99 ms | 66.36 ms | 1.5× | 2.0× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 64.24 ms | 54.08 ms | 44.85 ms | 1.2× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 132.15 ms | 151.72 ms | 55.18 ms | 0.9× | 2.4× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 90.27 ms | 79.95 ms | 45.89 ms | 1.1× | 2.0× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 90.51–93.81 ms | 47.22–51.32 ms | 45.99–50.40 ms |
| heap-sort | 90.12–94.73 ms | 59.78–64.00 ms | 50.97–54.47 ms |
| stack | 29.47–31.89 ms | 16.18–24.37 ms | 9.09–10.72 ms |
| queue | 31.16–34.10 ms | 16.24–32.45 ms | 8.89–10.71 ms |
| min-heap | 130.41–140.18 ms | 83.33–110.69 ms | 64.85–73.69 ms |
| dsu | 63.82–68.29 ms | 53.28–59.71 ms | 44.11–49.57 ms |
| bfs | 128.87–135.75 ms | 133.86–178.94 ms | 54.22–58.74 ms |
| dijkstra | 89.33–96.23 ms | 78.48–90.36 ms | 45.06–54.15 ms |

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
