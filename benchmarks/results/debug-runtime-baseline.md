# Archived debug-runtime baseline

Status: retained as toolchain-configuration evidence; do not compare this table
as optimized Ruda versus Go/Rust.

Generated on 2026-08-18 on Apple M2 with three measured samples after one
warm-up run. The harness invoked `build/debug/ruda build --release`: generated C
used `-O2`, but the output linked the unoptimized native runtime archive embedded
by the debug compiler build. The Ruda DSU inline benchmark also lacked path
compression in this archived run.

| Algorithm | Ruda median | Go median | Rust median |
|---|---:|---:|---:|
| insertion | 17915.10 ms | 29.95 ms | 28.38 ms |
| heap sort | 4481.92 ms | 39.77 ms | 22.56 ms |
| stack | 246.54 ms | 15.51 ms | 9.32 ms |
| queue | 274.29 ms | 15.54 ms | 9.38 ms |
| min-heap | 5175.26 ms | 55.58 ms | 31.14 ms |
| DSU | 7225.68 ms | 25.26 ms | 22.08 ms |
| BFS | 9982.56 ms | 61.47 ms | 24.31 ms |
| Dijkstra | 3952.96 ms | 41.79 ms | 39.64 ms |

The current valid release-runtime comparison is in [`latest.md`](latest.md).
This archive exists to prevent the original numbers from being mistaken for
lost or silently rewritten evidence.
