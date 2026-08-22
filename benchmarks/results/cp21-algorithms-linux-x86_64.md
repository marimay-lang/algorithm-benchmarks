# Latest algorithm benchmark

Generated: `2026-08-22T05:10:50+00:00`

Host: `Linux 6.12.57+deb13-amd64 x86_64`; CPU: `QEMU Virtual CPU version 2.5+`.

Ruda compiler executable: `/workspace/OS/ruda-algotithms/Ma/build/release/ruda`.

Ruda source revision: `1d728451612f5ad4d6cfb78a5785b2e57605af26`.

Algorithm corpus revision: `c8da4676e0e80522d795a6b7fe551e93916c9fad`.

Equivalence manifest: `benchmarks/equivalence.json` (`51702f2ad1bae31fb11b9df8550f58b2034e1e7044f3d6e7448e5001399d3535`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Ruda / Go | Ruda / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 6017.34 ms | 42.01 ms | 40.67 ms | 143.2× | 148.0× | Rust |
| heap-sort | 5 × 100,000 generated integers | 1652.21 ms | 52.96 ms | 44.34 ms | 31.2× | 37.3× | Rust |
| stack | 1,000,000 push + pop | 513.27 ms | 14.54 ms | 8.41 ms | 35.3× | 61.0× | Rust |
| queue | 1,000,000 enqueue + dequeue | 597.22 ms | 16.01 ms | 8.18 ms | 37.3× | 73.0× | Rust |
| min-heap | 500,000 insert + remove-min | 3309.05 ms | 75.14 ms | 57.16 ms | 44.0× | 57.9× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 3241.13 ms | 47.48 ms | 39.16 ms | 68.3× | 82.8× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 4442.56 ms | 111.13 ms | 47.56 ms | 40.0× | 93.4× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 1833.24 ms | 69.07 ms | 39.64 ms | 26.5× | 46.2× | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 5965.10–6624.60 ms | 40.94–44.38 ms | 38.91–45.54 ms |
| heap-sort | 1632.70–1814.83 ms | 50.72–56.58 ms | 43.54–48.45 ms |
| stack | 507.39–559.79 ms | 13.95–17.71 ms | 7.91–8.68 ms |
| queue | 584.50–656.68 ms | 13.98–18.37 ms | 7.57–8.84 ms |
| min-heap | 3265.97–3637.60 ms | 72.63–80.32 ms | 55.50–61.84 ms |
| dsu | 3212.65–3571.37 ms | 46.40–50.79 ms | 37.53–43.62 ms |
| bfs | 4370.78–5064.33 ms | 103.29–136.04 ms | 45.62–53.24 ms |
| dijkstra | 1811.51–2019.43 ms | 66.73–75.18 ms | 38.37–42.27 ms |

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
