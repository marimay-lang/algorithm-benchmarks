# Catalogue and language benchmark

Generated: 2026-09-09T10:58:32+07:00; profile: **standard**; scope: **local-only**; status: **failed**.

Host: Darwin arm64; Apple M2.

Samples: **3** after **0** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

**Diagnostic/correctness run: no performance or parity conclusion.**

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | Marimay VM (source run) ms |
|---|---|---|---|---|---|
| title-search-10k | 10,000 × 128 | 9.55 | 4.21 | 5.04 | 219.82 |
| title-search-100k | 100,000 × 128 | 74.77 | 15.39 | 19.11 | 1595.56 |
| normalize-title | 10,000 × 1 | 57.91 | 9.01 | 10.84 | 307.93 |
| word-frequency | 10,000 × 10 | 137.97 | 18.29 | 30.19 | 546.67 |
| report-builder | 10,000 × 1 | 15.30 | 5.31 | 5.29 | 234.00 |
| report-concat | 10,000 × 1 | 99.74 | 81.70 | 47.71 | **FAILED** |
| map-int | 4,096 × 32 | 8.20 | 5.31 | 6.18 | 134.00 |
| map-string | 4,096 × 32 | 22.88 | 6.97 | 9.96 | 194.02 |
| map-string-book | 10,000 × 4 | 31.47 | 6.68 | 10.27 | 172.45 |
| set-string-churn | 4,096 × 8 | 47.39 | 9.86 | 18.12 | 196.50 |
| catalog-match | 10,000 × 32 | 14.64 | 4.87 | 3.98 | 398.31 |
| catalog-dotcall | 10,000 × 32 | 8.06 | 4.71 | 3.72 | 316.76 |
| catalog-interface | 10,000 × 32 | 12.66 | 4.94 | 3.84 | 394.32 |
| record-reference-copy | 1,024 × 128 | 9.21 | 4.49 | 3.95 | 259.39 |
| record-create | 1,024 × 128 | 25.11 | 7.09 | 6.20 | 308.71 |
| array-grow | 100,000 × 4 | 6.77 | 6.31 | 4.04 | 357.19 |
| array-reserved | 100,000 × 4 | 7.43 | 5.49 | 4.18 | 359.34 |
| bfs-int | 4,096 × 16 | 8.05 | 5.49 | 5.09 | 529.62 |
| bfs-record | 4,096 × 16 | 560.14 | 6.69 | 4.71 | 534.17 |
| catalog-pipeline | 10,000 × 16 | 39.42 | 8.04 | 10.06 | 886.76 |
| parse-result | 10,000 × 8 | 19.82 | 5.97 | 5.77 | 151.05 |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.05 | 597.29 | 9.50–606.79 | 6256% |
| title-search-10k | Go native | 0.07 | 23.94 | 4.14–28.08 | 568% |
| title-search-10k | Rust native | 0.17 | 247.37 | 4.86–252.23 | 4909% |
| title-search-10k | Marimay VM (source run) | 2.67 | 25.70 | 217.15–242.85 | 12% |
| title-search-100k | Marimay native | 1.24 | 5.50 | 73.53–79.03 | 7% |
| title-search-100k | Go native | 0.41 | 0.96 | 14.84–15.80 | 8% |
| title-search-100k | Rust native | 0.51 | 1.75 | 17.86–19.61 | 9% |
| title-search-100k | Marimay VM (source run) | 43.30 | 130.28 | 1508.59–1638.87 | 8% |
| normalize-title | Marimay native | 0.06 | 0.64 | 57.84–58.48 | 2% |
| normalize-title | Go native | 0.00 | 0.02 | 9.01–9.02 | 2% |
| normalize-title | Rust native | 0.07 | 0.23 | 10.68–10.91 | 2% |
| normalize-title | Marimay VM (source run) | 0.21 | 0.94 | 307.72–308.66 | 2% |
| word-frequency | Marimay native | 0.35 | 1.26 | 137.06–138.32 | 2% |
| word-frequency | Go native | 0.01 | 0.22 | 18.28–18.50 | 2% |
| word-frequency | Rust native | 0.08 | 0.21 | 30.07–30.28 | 2% |
| word-frequency | Marimay VM (source run) | 2.18 | 88.95 | 544.48–633.43 | 16% |
| report-builder | Marimay native | 0.05 | 0.10 | 15.25–15.35 | 2% |
| report-builder | Go native | 0.06 | 0.24 | 5.13–5.37 | 5% |
| report-builder | Rust native | 0.38 | 0.96 | 4.91–5.87 | 22% |
| report-builder | Marimay VM (source run) | 0.51 | 2.35 | 233.49–235.84 | 2% |
| report-concat | Marimay native | 2.39 | 7.83 | 97.35–105.18 | 8% |
| report-concat | Go native | 0.30 | 1.75 | 80.25–82.01 | 2% |
| report-concat | Rust native | 0.15 | 1.17 | 47.56–48.73 | 2% |
| map-int | Marimay native | 0.31 | 0.66 | 7.85–8.50 | 11% |
| map-int | Go native | 0.05 | 0.46 | 4.90–5.36 | 9% |
| map-int | Rust native | 0.13 | 1.06 | 5.26–6.31 | 17% |
| map-int | Marimay VM (source run) | 0.10 | 0.35 | 133.90–134.26 | 2% |
| map-string | Marimay native | 0.04 | 0.44 | 22.84–23.28 | 2% |
| map-string | Go native | 0.10 | 0.25 | 6.87–7.12 | 5% |
| map-string | Rust native | 0.05 | 0.11 | 9.91–10.02 | 2% |
| map-string | Marimay VM (source run) | 0.11 | 0.68 | 193.45–194.13 | 2% |
| map-string-book | Marimay native | 0.01 | 0.40 | 31.45–31.86 | 2% |
| map-string-book | Go native | 0.05 | 0.43 | 6.30–6.73 | 7% |
| map-string-book | Rust native | 0.02 | 0.13 | 10.26–10.39 | 2% |
| map-string-book | Marimay VM (source run) | 0.25 | 0.97 | 172.20–173.17 | 2% |
| set-string-churn | Marimay native | 0.27 | 0.95 | 46.71–47.66 | 2% |
| set-string-churn | Go native | 0.05 | 0.37 | 9.81–10.18 | 4% |
| set-string-churn | Rust native | 0.08 | 0.25 | 17.96–18.20 | 2% |
| set-string-churn | Marimay VM (source run) | 2.05 | 4.38 | 194.46–198.84 | 3% |
| catalog-match | Marimay native | 0.11 | 2.85 | 14.53–17.38 | 19% |
| catalog-match | Go native | 0.25 | 1.98 | 4.63–6.60 | 41% |
| catalog-match | Rust native | 0.18 | 0.40 | 3.80–4.20 | 14% |
| catalog-match | Marimay VM (source run) | 0.98 | 2.63 | 397.33–399.96 | 2% |
| catalog-dotcall | Marimay native | 0.08 | 0.27 | 7.98–8.25 | 3% |
| catalog-dotcall | Go native | 0.07 | 0.55 | 4.22–4.77 | 12% |
| catalog-dotcall | Rust native | 0.02 | 0.13 | 3.69–3.83 | 4% |
| catalog-dotcall | Marimay VM (source run) | 0.97 | 2.44 | 315.29–317.73 | 2% |
| catalog-interface | Marimay native | 0.10 | 0.31 | 12.45–12.76 | 2% |
| catalog-interface | Go native | 0.08 | 0.43 | 4.59–5.02 | 9% |
| catalog-interface | Rust native | 0.13 | 0.26 | 3.71–3.97 | 10% |
| catalog-interface | Marimay VM (source run) | 0.08 | 0.78 | 394.24–395.02 | 2% |
| record-reference-copy | Marimay native | 0.02 | 0.05 | 9.19–9.24 | 2% |
| record-reference-copy | Go native | 0.06 | 0.39 | 4.43–4.82 | 9% |
| record-reference-copy | Rust native | 0.03 | 0.06 | 3.92–3.98 | 2% |
| record-reference-copy | Marimay VM (source run) | 1.20 | 3.22 | 257.37–260.58 | 2% |
| record-create | Marimay native | 0.13 | 0.48 | 24.77–25.24 | 2% |
| record-create | Go native | 0.06 | 0.15 | 7.00–7.15 | 3% |
| record-create | Rust native | 0.16 | 0.44 | 6.03–6.48 | 8% |
| record-create | Marimay VM (source run) | 0.17 | 2.33 | 308.54–310.87 | 2% |
| array-grow | Marimay native | 0.08 | 0.18 | 6.67–6.85 | 3% |
| array-grow | Go native | 0.09 | 0.24 | 6.16–6.40 | 4% |
| array-grow | Rust native | 0.08 | 0.30 | 3.96–4.26 | 7% |
| array-grow | Marimay VM (source run) | 1.10 | 4.09 | 356.09–360.18 | 2% |
| array-reserved | Marimay native | 0.03 | 0.17 | 7.29–7.46 | 2% |
| array-reserved | Go native | 0.05 | 0.17 | 5.44–5.61 | 3% |
| array-reserved | Rust native | 0.13 | 0.45 | 3.86–4.31 | 11% |
| array-reserved | Marimay VM (source run) | 0.93 | 5.07 | 355.20–360.27 | 2% |
| bfs-int | Marimay native | 0.03 | 0.18 | 8.02–8.20 | 2% |
| bfs-int | Go native | 0.10 | 0.27 | 5.39–5.66 | 5% |
| bfs-int | Rust native | 0.03 | 0.16 | 4.95–5.11 | 3% |
| bfs-int | Marimay VM (source run) | 0.80 | 6.45 | 523.97–530.42 | 2% |
| bfs-record | Marimay native | 2.18 | 6.39 | 555.94–562.33 | 2% |
| bfs-record | Go native | 0.23 | 0.49 | 6.46–6.95 | 11% |
| bfs-record | Rust native | 0.11 | 0.26 | 4.61–4.87 | 7% |
| bfs-record | Marimay VM (source run) | 2.81 | 11.42 | 531.36–542.78 | 2% |
| catalog-pipeline | Marimay native | 0.02 | 0.27 | 39.17–39.44 | 2% |
| catalog-pipeline | Go native | 0.03 | 0.33 | 7.74–8.07 | 4% |
| catalog-pipeline | Rust native | 0.05 | 0.20 | 10.01–10.21 | 2% |
| catalog-pipeline | Marimay VM (source run) | 3.62 | 8.45 | 881.93–890.38 | 2% |
| parse-result | Marimay native | 0.02 | 0.30 | 19.55–19.85 | 2% |
| parse-result | Go native | 0.04 | 0.29 | 5.93–6.22 | 5% |
| parse-result | Rust native | 0.00 | 0.15 | 5.77–5.92 | 3% |
| parse-result | Marimay VM (source run) | 0.10 | 1.36 | 149.80–151.16 | 2% |

## Failed cells

The first failed observation is retained; remaining scheduled runs of that cell are marked skipped. Successful observations before a failure remain in JSON but have no summary or ratio.

### report-concat / Marimay VM (source run)

```text
benchmark exited 70: /path/to/Marimay/marimay/build/release/mmay run /path/to/Marimay/algorithm-benchmarks/marimay/catalog --engine vm --max-heap-bytes 67108864 -- report-concat 10000 1
error[I0002]: VM execution failed a resource, integrity, or host requirement

```


## Coverage and representations

- **title-search-10k**: Linear exact UTF-8 title search; 75% hits and 25% misses.
- **title-search-100k**: Same queries over 100,000 unique runtime-built titles.
- **normalize-title**: ASCII trim, owned scalar pieces, explicit ASCII/Russian folding table, builder, equality.
- **word-frequency**: Four-token Russian/ASCII lines; owned token split and map counts; all keys checked.
- **report-builder**: Build 10k formatted rows using a growing string builder; checksum every UTF-8 byte.
- **report-concat**: Same rows with a fresh immutable concatenation each step (quadratic copy volume).
- **map-int**: 4096 integer keys, get then put; deterministic permutation and full weighted histogram.
- **map-string**: Same map trace with dynamic Russian/ASCII title keys; fresh equal keys for final lookups.
- **map-string-book**: Dynamic string keys to Book references; construct once, lookup and read title/state/serial.
- **set-string-churn**: Sliding live window; remove old string, check absence, insert fresh key; verify final membership.
- **catalog-match**: BookState enum + exhaustive match; Go tagged struct + switch, Rust enum + match.
- **catalog-dotcall**: Concrete Book label call; no per-call result string allocation.
- **catalog-interface**: Materialized interface array; method-table call and UTF-8 label length.
- **record-reference-copy**: Retain aliases in a growing array; compare every identity and read fields.
- **record-create**: Retain fresh Book objects per batch; same fields, distinct identity; titles/states shared.
- **array-grow**: Append integers from empty capacity, then checksum all values.
- **array-reserved**: Same append trace with one initial reserve.
- **bfs-int**: Contiguous integer IDs, growing integer queue, distance array, degree 16.
- **bfs-record**: Same edges/distances; Node records and reference queue; edges remain integer IDs.
- **catalog-pipeline**: Combined title search, title frequency map, and BookState match; 25% missing queries.
- **parse-result**: Format/parse decimal tokens, 25% invalid suffixes; propagate Result/error then match.

## Interpretation limits

- No general Unicode lower/casefold API: normalize-title measures a shared corpus folding helper only.
- No I/O, concurrency, JSON or HTTP claims.
- Allocation workloads prescribe escaping objects; allocation counts, GC pauses and peak RSS are not measured.
- Map/set implementations retain host ordering, hashing, growth and GC policies. Cross-language equality is observable results, not identical runtime layouts.
- Go uses *Book and Rust Rc<Book> to preserve Marimay reference identity; Rust Rc costs do not generalize to all Rust representations.
- BFS has fixed degree 16 and contiguous IDs; it is not an O(V²)-edge dense graph and record edges are IDs, not object pointers.
- The per-workload Go targets are exploratory thresholds, not reviewed release budgets. No average score or general ‘Go parity’ verdict is computed.
- Short cases can be dominated by process startup and validation; repeat with larger documented inputs before attributing a difference to dispatch, GC or a particular primitive.
- Interface results include array construction/boxing and compiler devirtualization opportunities; they are not isolated virtual-call latency.

## Toolchains

- python: `3.9.6`
- marimay: `Marimay compiler 0.1.0-alpha.1`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`

Command: `benchmarks/catalog_bench.py --profile standard --verify-only --output benchmarks/results/catalog-standard-check-local.md`
