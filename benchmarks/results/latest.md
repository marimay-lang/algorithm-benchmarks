# Latest algorithm benchmark

Generated: `2026-08-21T20:28:10+07:00`

Host: `macOS-26.3.1-arm64-arm-64bit`; CPU: `Apple M2`.

Ruda compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/ruda`.

Samples: 5 measured after 2 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Ruda median | Go median | Rust median | Fastest |
|---|---|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 4040.81 ms | 30.16 ms | 29.15 ms | Rust |
| heap-sort | 5 × 100,000 generated integers | 1008.80 ms | 40.47 ms | 22.58 ms | Rust |
| stack | 1,000,000 push + pop | 394.00 ms | 15.78 ms | 9.91 ms | Rust |
| queue | 1,000,000 enqueue + dequeue | 425.90 ms | 15.32 ms | 9.22 ms | Rust |
| min-heap | 500,000 insert + remove-min | 1865.05 ms | 54.25 ms | 30.22 ms | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 1981.23 ms | 25.83 ms | 22.92 ms | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 2456.67 ms | 62.76 ms | 24.50 ms | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 885.73 ms | 41.54 ms | 39.57 ms | Rust |

## Range (min–max)

| Algorithm | Ruda | Go | Rust |
|---|---:|---:|---:|
| insertion | 3998.55–4084.48 ms | 29.12–31.11 ms | 28.35–29.57 ms |
| heap-sort | 985.95–1049.32 ms | 39.08–41.51 ms | 22.13–23.25 ms |
| stack | 382.01–408.85 ms | 15.69–16.58 ms | 9.79–10.21 ms |
| queue | 422.34–437.81 ms | 14.93–16.08 ms | 8.96–9.46 ms |
| min-heap | 1860.65–1866.06 ms | 53.71–55.06 ms | 29.92–30.95 ms |
| dsu | 1968.61–2135.71 ms | 24.74–26.33 ms | 21.70–23.10 ms |
| bfs | 2451.77–2497.43 ms | 57.87–64.08 ms | 24.03–26.35 ms |
| dijkstra | 885.14–897.14 ms | 40.82–43.97 ms | 39.47–40.23 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- All three languages call reusable sorting, structures, and graph packages.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  Ruda and Rust model absence with Option while Go returns a value/bool pair.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- Ruda: `Ruda compiler 0.0.0-dev`
- Go: `go version go1.26.4 darwin/arm64`
- Rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
