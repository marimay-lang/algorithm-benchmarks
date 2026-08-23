# Latest algorithm benchmark

Generated: `2026-08-22T16:27:37+07:00`

Host: `Darwin 25.3.0 arm64`; CPU: `Apple M2`.

Marimay compiler executable: `/home/marimay/Projects/ai-projects/Ma/build/release/mmay`.

Marimay source revision: `17b7a1f1dcffd17659d84244c5f9981cdba867ea`.

Algorithm corpus revision: `1e7dbf794b57eb43d27dec401b066ffa8771d978`.

Equivalence manifest: `benchmarks/equivalence.json` (`bf2f251de2d91e22d6696a50aa83babe9d1497139a305c4e1770e09c1f2f7e9b`).

Samples: 11 measured after 3 warm-up runs. Reported times include process startup and one fixed checksum line; compilation is excluded.

| Algorithm | Workload | Marimay median | Go median | Rust median | Marimay / Go | Marimay / Rust | Fastest |
|---|---|---:|---:|---:|---:|---:|---:|
| insertion | 50 × 2,500 generated integers | 2956.20 ms | 29.85 ms | 28.16 ms | 99.0× | 105.0× | Rust |
| heap-sort | 5 × 100,000 generated integers | 722.53 ms | 39.50 ms | 21.94 ms | 18.3× | 32.9× | Rust |
| stack | 1,000,000 push + pop | 353.22 ms | 15.51 ms | 9.17 ms | 22.8× | 38.5× | Rust |
| queue | 1,000,000 enqueue + dequeue | 379.31 ms | 15.28 ms | 9.21 ms | 24.8× | 41.2× | Rust |
| min-heap | 500,000 insert + remove-min | 1474.64 ms | 55.20 ms | 30.44 ms | 26.7× | 48.4× | Rust |
| dsu | 100,000 nodes; 5,000,000 unions | 1593.74 ms | 24.91 ms | 22.11 ms | 64.0× | 72.1× | Rust |
| bfs | 300 × 20,000 nodes, degree 4 | 2167.78 ms | 62.42 ms | 24.08 ms | 34.7× | 90.0× | Rust |
| dijkstra | 80 × 800 nodes, O(V²) | 672.39 ms | 41.20 ms | 39.30 ms | 16.3× | 17.1× | Rust |

## Range (min–max)

| Algorithm | Marimay | Go | Rust |
|---|---:|---:|---:|
| insertion | 2940.89–3094.36 ms | 28.96–30.56 ms | 27.91–29.51 ms |
| heap-sort | 715.22–768.52 ms | 38.70–41.07 ms | 21.77–23.14 ms |
| stack | 346.54–363.00 ms | 14.17–16.98 ms | 8.91–10.50 ms |
| queue | 371.69–390.96 ms | 15.07–15.87 ms | 8.88–9.98 ms |
| min-heap | 1460.25–1516.33 ms | 52.85–58.61 ms | 29.29–32.68 ms |
| dsu | 1581.11–1627.90 ms | 24.23–26.31 ms | 21.63–33.37 ms |
| bfs | 2154.74–2356.22 ms | 61.04–65.73 ms | 23.51–27.16 ms |
| dijkstra | 669.66–699.60 ms | 40.67–42.62 ms | 38.80–40.29 ms |

## Interpretation limits

- Checksums prove matching selected results, not identical abstraction boundaries.
- All three languages call reusable sorting, structures, and graph packages.
- Stack, queue, heap, DSU, BFS, and O(V²) Dijkstra use matching operations and layouts;
  Marimay and Rust model absence with Option while Go returns a value/bool pair.
- Checksums cover selected results and do not prove equal compiler optimization maturity.


## Toolchains

- python: `3.9.6`
- marimay: `Marimay compiler 0.0.0-dev`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Checksums are identical across every language and every measured run. These are local comparative numbers, not stable language performance claims.
