# Latest algorithm benchmark

Generated: `2026-08-22T05:30:24+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Ruda compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/ruda`.

Ruda source revision: `1d728451612f5ad4d6cfb78a5785b2e57605af26`.

Algorithm corpus revision: `a05a1ffff0e6be52cda6deac0c64e7215048e91d`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 6968.71 ms | 48.61 ms | 46.67 ms | 143.4× | 149.3× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1933.01 ms | 59.65 ms | 51.93 ms | 32.4× | 37.2× | Rust |
| stack | 1,000,000 push + pop | 589.93 ms | 18.58 ms | 10.49 ms | 31.8× | 56.2× | Rust |
| queue | 1,000,000 enqueue + dequeue | 676.86 ms | 21.17 ms | 9.26 ms | 32.0× | 73.1× | Rust |
| min-heap | 500,000 insert + remove-min | 3864.02 ms | 87.29 ms | 66.98 ms | 44.3× | 57.7× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 3882.68 ms | 54.55 ms | 43.96 ms | 71.2× | 88.3× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 5547.00 ms | 140.75 ms | 54.78 ms | 39.4× | 101.3× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 2128.03 ms | 78.04 ms | 45.96 ms | 27.3× | 46.3× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 6597.60–7679.31 ms | 46.67–80.71 ms | 44.82–53.54 ms |
| heap-sort | 1871.74–2120.99 ms | 55.00–70.23 ms | 47.93–57.49 ms |
| stack | 565.21–659.64 ms | 17.13–57.23 ms | 8.46–14.83 ms |
| queue | 649.86–710.23 ms | 16.22–40.40 ms | 8.31–11.81 ms |
| min-heap | 3640.50–3903.40 ms | 80.30–97.68 ms | 62.59–79.06 ms |
| dsu | 3671.89–4164.90 ms | 51.36–63.25 ms | 42.43–51.51 ms |
| bfs | 5388.29–6020.37 ms | 120.67–243.91 ms | 53.33–86.73 ms |
| dijkstra | 2017.39–2329.32 ms | 73.52–84.80 ms | 42.69–55.82 ms |

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
