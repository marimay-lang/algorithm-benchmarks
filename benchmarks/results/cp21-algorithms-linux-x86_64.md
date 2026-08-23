# Latest algorithm benchmark

Generated: `2026-08-23T03:56:22+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Marimay compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/mmay`.

Marimay source revision: `589e19d807e709c9bbca242642b00d80a880f82e`.

Algorithm corpus revision: `2fa0cb206131be1da5bb290945a9da45ba2cbf8e`.

Equivalence manifest: `benchmarks/equivalence.json` (`bf2f251de2d91e22d6696a50aa83babe9d1497139a305c4e1770e09c1f2f7e9b`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 61.07 ms | 41.90 ms | 40.36 ms | 1.5× | 1.5× | Rust |
| heap-sort | 5 × 100,000 generated integers | 79.39 ms | 52.15 ms | 44.06 ms | 1.5× | 1.8× | Rust |
| stack | 1,000,000 push + pop | 25.89 ms | 14.27 ms | 7.90 ms | 1.8× | 3.3× | Rust |
| queue | 1,000,000 enqueue + dequeue | 27.17 ms | 14.72 ms | 7.76 ms | 1.8× | 3.5× | Rust |
| min-heap | 500,000 insert + remove-min | 113.76 ms | 73.66 ms | 56.97 ms | 1.5× | 2.0× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 55.28 ms | 47.25 ms | 38.62 ms | 1.2× | 1.4× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 112.40 ms | 106.68 ms | 48.37 ms | 1.1× | 2.3× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 78.13 ms | 68.48 ms | 39.36 ms | 1.1× | 2.0× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 60.45–64.16 ms | 40.94–49.23 ms | 39.65–40.96 ms |
| heap-sort | 78.19–81.07 ms | 51.25–54.31 ms | 42.84–46.23 ms |
| stack | 25.43–27.55 ms | 13.83–16.02 ms | 7.29–8.41 ms |
| queue | 26.05–28.56 ms | 13.44–18.00 ms | 7.21–8.40 ms |
| min-heap | 111.52–123.02 ms | 72.22–76.15 ms | 55.85–62.34 ms |
| dsu | 54.88–57.58 ms | 46.19–49.26 ms | 37.44–39.45 ms |
| bfs | 110.44–116.40 ms | 104.53–111.16 ms | 46.91–53.59 ms |
| dijkstra | 76.90–84.35 ms | 66.65–70.98 ms | 38.44–41.16 ms |

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
