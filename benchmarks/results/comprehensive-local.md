# Catalogue and language benchmark

Generated: 2026-09-10T14:48:11+07:00; profile: **standard**; scope: **local-only**; status: **passed**.

Host: Darwin arm64; Apple M2.

Samples: **11** after **3** process warmups; timeout: 300 s; Marimay managed heap: 67108864 bytes.

Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.

Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.

Bun runs TypeScript source with JavaScriptCore JIT and default GC. Each observation starts a fresh process; TypeScript loading/transpilation and JIT work are included. Process warmups do not retain a warmed JIT. Bun is not a native AOT column. See the representation differences in the catalogue methodology.

| Workload | Size × rounds | Marimay native ms | Go native ms | Rust native ms | Marimay VM (source run) ms | Bun / TypeScript ms | native / Go | native / Rust | Go target | Assessment |
|---|---|---|---|---|---|---|---|---|---|---|
| title-search-10k | 10,000 × 128 | 9.18 | 4.41 | 4.43 | 153.30 | 12.59 | 2.08× | 2.07× | — | measured |
| title-search-100k | 100,000 × 128 | 70.71 | 15.07 | 16.84 | 904.26 | 35.84 | 4.69× | 4.20× | — | measured |
| normalize-title | 10,000 × 1 | 53.91 | 8.84 | 10.27 | 224.09 | 17.42 | 6.10× | 5.25× | — | measured |
| word-frequency | 10,000 × 10 | 136.82 | 18.57 | 27.88 | 398.29 | 18.29 | 7.37× | 4.91× | ≤ 2.0× | above target |
| report-builder | 10,000 × 1 | 14.21 | 5.20 | 5.37 | 183.80 | 12.20 | 2.73× | 2.65× | — | measured |
| report-concat | 10,000 × 1 | 96.05 | 81.02 | 46.56 | 259.77 | 12.05 | 1.19× | 2.06× | — | measured |
| map-int | 4,096 × 32 | 7.59 | 5.20 | 5.98 | 112.10 | 13.29 | 1.46× | 1.27× | ≤ 1.5× | within target |
| map-string | 4,096 × 32 | 23.01 | 7.14 | 9.99 | 141.56 | 14.69 | 3.22× | 2.30× | ≤ 2.0× | above target |
| map-string-book | 10,000 × 4 | 28.84 | 6.43 | 10.23 | 152.88 | 14.74 | 4.48× | 2.82× | — | measured |
| set-string-churn | 4,096 × 8 | 43.32 | 10.04 | 16.52 | 156.24 | 17.27 | 4.31× | 2.62× | — | measured |
| catalog-match | 10,000 × 32 | 13.73 | 4.79 | 3.97 | 350.57 | 19.27 | 2.87× | 3.46× | ≤ 1.5× | above target |
| catalog-dotcall | 10,000 × 32 | 8.64 | 4.67 | 3.77 | 278.71 | 18.02 | 1.85× | 2.29× | — | measured |
| catalog-interface | 10,000 × 32 | 12.22 | 4.88 | 4.01 | 369.57 | 18.08 | 2.50× | 3.05× | — | measured |
| record-reference-copy | 1,024 × 128 | 7.05 | 4.51 | 3.36 | 205.44 | 14.06 | 1.56× | 2.10× | — | measured |
| record-create | 1,024 × 128 | 21.39 | 6.83 | 6.11 | 240.07 | 15.39 | 3.13× | 3.50× | — | measured |
| array-grow | 100,000 × 4 | 6.97 | 6.59 | 4.12 | 226.76 | 13.56 | 1.06× | 1.69× | — | measured |
| array-reserved | 100,000 × 4 | 6.86 | 5.18 | 4.28 | 226.08 | 12.47 | 1.32× | 1.60× | — | measured |
| bfs-int | 4,096 × 16 | 7.59 | 5.41 | 4.58 | 229.65 | 16.51 | 1.40× | 1.66× | — | measured |
| bfs-record | 4,096 × 16 | 9.41 | 5.91 | 4.73 | 246.36 | 16.76 | 1.59× | 1.99× | — | measured |
| catalog-pipeline | 10,000 × 16 | 37.85 | 8.13 | 10.27 | 564.06 | 22.59 | 4.65× | 3.68× | — | measured |
| parse-result | 10,000 × 8 | 17.90 | 6.10 | 5.54 | 134.65 | 12.75 | 2.93× | 3.23× | — | measured |
| insertion | fixed anchor | 52.17 | 29.29 | 28.87 | 6081.22 | 81.33 | 1.78× | 1.81× | — | measured |
| heap-sort | fixed anchor | 32.42 | 39.31 | 22.77 | 1676.59 | 91.75 | 0.82× | 1.42× | ≤ 1.3× | within target |
| stack | fixed anchor | 9.94 | 14.85 | 8.94 | 1044.16 | 21.85 | 0.67× | 1.11× | ≤ 1.3× | within target |
| queue | fixed anchor | 10.16 | 14.57 | 9.01 | 1155.52 | 25.54 | 0.70× | 1.13× | ≤ 1.3× | within target |
| min-heap | fixed anchor | 46.21 | 53.68 | 29.79 | 5682.29 | 107.91 | 0.86× | 1.55× | ≤ 1.3× | within target |
| dsu | fixed anchor | 30.13 | 24.39 | 22.26 | 5437.59 | 48.68 | 1.24× | 1.35× | — | measured |
| bfs | fixed anchor | 66.17 | 62.02 | 23.66 | 5521.00 | 67.78 | 1.07× | 2.80× | — | measured |
| dijkstra | fixed anchor | 41.49 | 41.06 | 39.04 | 2399.32 | 75.60 | 1.01× | 1.06× | ≤ 1.3× | within target |
| frequency-map | fixed anchor | 32.72 | 14.04 | 23.77 | 476.73 | 27.36 | 2.33× | 1.38× | — | noisy; repeat |
| unique-set | fixed anchor | 27.38 | 16.32 | 18.98 | 351.43 | 21.49 | 1.68× | 1.44× | — | measured |
| rune-frequency | fixed anchor | 22.65 | 5.89 | 6.24 | 249.33 | 16.43 | 3.84× | 3.63× | — | measured |

## Dispersion

| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |
|---|---|---:|---:|---:|---:|
| title-search-10k | Marimay native | 0.15 | 0.30 | 8.98–10.17 | 5% |
| title-search-10k | Go native | 0.11 | 0.26 | 4.02–9.49 | 7% |
| title-search-10k | Rust native | 0.24 | 0.72 | 4.15–6.01 | 16% |
| title-search-10k | Marimay VM (source run) | 1.34 | 3.41 | 151.25–157.30 | 3% |
| title-search-10k | Bun / TypeScript | 0.45 | 1.72 | 12.13–16.99 | 14% |
| title-search-100k | Marimay native | 0.61 | 2.16 | 70.10–73.51 | 3% |
| title-search-100k | Go native | 0.32 | 0.77 | 13.90–16.77 | 6% |
| title-search-100k | Rust native | 0.16 | 0.27 | 16.68–18.37 | 3% |
| title-search-100k | Marimay VM (source run) | 11.91 | 27.58 | 887.62–1014.44 | 4% |
| title-search-100k | Bun / TypeScript | 0.54 | 0.80 | 35.28–37.18 | 5% |
| normalize-title | Marimay native | 0.47 | 1.23 | 53.16–60.65 | 3% |
| normalize-title | Go native | 0.28 | 0.55 | 8.24–9.50 | 9% |
| normalize-title | Rust native | 0.27 | 0.51 | 9.90–10.78 | 8% |
| normalize-title | Marimay VM (source run) | 0.88 | 1.91 | 222.27–235.74 | 2% |
| normalize-title | Bun / TypeScript | 0.21 | 0.56 | 16.98–18.77 | 4% |
| word-frequency | Marimay native | 1.09 | 2.47 | 135.45–142.66 | 2% |
| word-frequency | Go native | 0.29 | 1.16 | 18.28–27.81 | 6% |
| word-frequency | Rust native | 0.24 | 0.61 | 27.24–28.54 | 3% |
| word-frequency | Marimay VM (source run) | 1.96 | 4.68 | 396.08–415.49 | 2% |
| word-frequency | Bun / TypeScript | 0.19 | 0.81 | 17.85–19.49 | 4% |
| report-builder | Marimay native | 0.15 | 0.36 | 13.71–15.26 | 3% |
| report-builder | Go native | 0.08 | 0.30 | 4.68–7.51 | 6% |
| report-builder | Rust native | 0.28 | 0.58 | 4.94–5.80 | 16% |
| report-builder | Marimay VM (source run) | 1.20 | 2.48 | 181.59–201.51 | 2% |
| report-builder | Bun / TypeScript | 0.66 | 1.41 | 11.29–13.78 | 16% |
| report-concat | Marimay native | 0.81 | 2.37 | 95.22–104.53 | 3% |
| report-concat | Go native | 0.86 | 2.30 | 78.84–82.36 | 3% |
| report-concat | Rust native | 0.28 | 1.53 | 46.09–52.05 | 3% |
| report-concat | Marimay VM (source run) | 2.03 | 8.55 | 256.45–428.68 | 3% |
| report-concat | Bun / TypeScript | 0.24 | 1.27 | 11.81–15.09 | 11% |
| map-int | Marimay native | 0.11 | 0.30 | 7.37–8.35 | 4% |
| map-int | Go native | 0.24 | 0.63 | 4.91–5.64 | 14% |
| map-int | Rust native | 0.34 | 0.57 | 5.63–6.50 | 17% |
| map-int | Marimay VM (source run) | 0.32 | 2.49 | 111.77–126.10 | 2% |
| map-int | Bun / TypeScript | 0.24 | 0.82 | 12.39–14.85 | 6% |
| map-string | Marimay native | 0.15 | 0.38 | 22.73–24.54 | 2% |
| map-string | Go native | 0.03 | 0.42 | 7.07–8.08 | 6% |
| map-string | Rust native | 0.15 | 0.62 | 9.64–11.07 | 6% |
| map-string | Marimay VM (source run) | 0.73 | 5.31 | 140.75–150.86 | 4% |
| map-string | Bun / TypeScript | 0.24 | 0.54 | 14.09–16.64 | 5% |
| map-string-book | Marimay native | 0.27 | 2.14 | 28.31–36.83 | 7% |
| map-string-book | Go native | 0.19 | 1.34 | 6.20–8.13 | 21% |
| map-string-book | Rust native | 0.30 | 0.60 | 9.83–11.13 | 9% |
| map-string-book | Marimay VM (source run) | 1.97 | 5.27 | 149.66–165.46 | 4% |
| map-string-book | Bun / TypeScript | 0.25 | 1.38 | 14.46–17.46 | 9% |
| set-string-churn | Marimay native | 0.54 | 3.76 | 42.02–48.31 | 9% |
| set-string-churn | Go native | 0.28 | 0.86 | 9.66–11.13 | 9% |
| set-string-churn | Rust native | 0.69 | 1.26 | 15.49–18.50 | 13% |
| set-string-churn | Marimay VM (source run) | 2.04 | 14.11 | 154.20–192.63 | 9% |
| set-string-churn | Bun / TypeScript | 0.42 | 3.34 | 16.66–21.60 | 19% |
| catalog-match | Marimay native | 0.28 | 0.72 | 13.04–15.04 | 6% |
| catalog-match | Go native | 0.15 | 0.23 | 4.48–6.00 | 9% |
| catalog-match | Rust native | 0.14 | 0.57 | 3.78–4.74 | 14% |
| catalog-match | Marimay VM (source run) | 3.35 | 9.31 | 346.24–364.57 | 3% |
| catalog-match | Bun / TypeScript | 0.69 | 1.40 | 17.85–21.10 | 11% |
| catalog-dotcall | Marimay native | 0.23 | 0.40 | 8.26–9.89 | 8% |
| catalog-dotcall | Go native | 0.23 | 0.47 | 4.37–4.97 | 15% |
| catalog-dotcall | Rust native | 0.15 | 0.77 | 3.61–5.03 | 20% |
| catalog-dotcall | Marimay VM (source run) | 6.11 | 12.57 | 272.16–287.86 | 7% |
| catalog-dotcall | Bun / TypeScript | 0.63 | 1.28 | 16.84–19.19 | 10% |
| catalog-interface | Marimay native | 0.13 | 0.40 | 11.91–13.36 | 3% |
| catalog-interface | Go native | 0.19 | 0.41 | 4.51–5.68 | 12% |
| catalog-interface | Rust native | 0.16 | 0.35 | 3.68–5.29 | 12% |
| catalog-interface | Marimay VM (source run) | 2.28 | 9.27 | 365.48–399.37 | 3% |
| catalog-interface | Bun / TypeScript | 0.54 | 1.76 | 17.21–19.59 | 10% |
| record-reference-copy | Marimay native | 0.09 | 0.23 | 6.70–7.64 | 4% |
| record-reference-copy | Go native | 0.25 | 0.55 | 4.22–5.68 | 17% |
| record-reference-copy | Rust native | 0.07 | 0.14 | 3.25–3.63 | 6% |
| record-reference-copy | Marimay VM (source run) | 0.54 | 6.71 | 203.68–226.11 | 3% |
| record-reference-copy | Bun / TypeScript | 0.46 | 1.45 | 13.52–15.57 | 10% |
| record-create | Marimay native | 0.27 | 2.39 | 21.02–26.18 | 11% |
| record-create | Go native | 0.22 | 0.71 | 6.52–8.46 | 10% |
| record-create | Rust native | 0.39 | 0.75 | 5.68–7.03 | 19% |
| record-create | Marimay VM (source run) | 4.49 | 13.91 | 235.57–364.24 | 6% |
| record-create | Bun / TypeScript | 0.35 | 2.48 | 14.74–18.14 | 16% |
| array-grow | Marimay native | 0.12 | 0.44 | 6.73–7.42 | 6% |
| array-grow | Go native | 0.21 | 0.61 | 6.29–7.26 | 10% |
| array-grow | Rust native | 0.13 | 0.60 | 3.99–5.51 | 15% |
| array-grow | Marimay VM (source run) | 5.41 | 11.38 | 218.59–237.51 | 7% |
| array-grow | Bun / TypeScript | 0.20 | 1.41 | 13.36–15.89 | 10% |
| array-reserved | Marimay native | 0.17 | 0.40 | 6.68–7.36 | 7% |
| array-reserved | Go native | 0.14 | 0.33 | 5.00–5.91 | 8% |
| array-reserved | Rust native | 0.27 | 0.71 | 3.91–5.23 | 19% |
| array-reserved | Marimay VM (source run) | 3.64 | 9.56 | 218.23–229.73 | 5% |
| array-reserved | Bun / TypeScript | 0.33 | 1.24 | 12.01–13.64 | 10% |
| bfs-int | Marimay native | 0.07 | 0.33 | 7.41–8.42 | 4% |
| bfs-int | Go native | 0.18 | 0.37 | 5.18–6.37 | 10% |
| bfs-int | Rust native | 0.28 | 0.66 | 4.27–26.21 | 19% |
| bfs-int | Marimay VM (source run) | 0.79 | 2.02 | 227.94–250.60 | 2% |
| bfs-int | Bun / TypeScript | 0.28 | 0.64 | 15.93–17.78 | 5% |
| bfs-record | Marimay native | 0.17 | 0.44 | 9.15–9.96 | 5% |
| bfs-record | Go native | 0.15 | 0.40 | 5.61–6.58 | 8% |
| bfs-record | Rust native | 0.07 | 0.40 | 4.59–5.17 | 8% |
| bfs-record | Marimay VM (source run) | 0.82 | 2.52 | 245.19–262.08 | 2% |
| bfs-record | Bun / TypeScript | 0.42 | 0.97 | 16.26–17.76 | 8% |
| catalog-pipeline | Marimay native | 0.16 | 0.64 | 37.45–40.86 | 2% |
| catalog-pipeline | Go native | 0.20 | 0.33 | 7.66–8.66 | 7% |
| catalog-pipeline | Rust native | 0.29 | 0.71 | 9.85–11.38 | 9% |
| catalog-pipeline | Marimay VM (source run) | 1.62 | 15.17 | 562.23–717.22 | 3% |
| catalog-pipeline | Bun / TypeScript | 0.39 | 1.11 | 22.06–24.47 | 5% |
| parse-result | Marimay native | 0.20 | 0.55 | 17.68–19.65 | 3% |
| parse-result | Go native | 0.16 | 0.75 | 5.57–11.38 | 12% |
| parse-result | Rust native | 0.18 | 0.33 | 5.29–7.41 | 10% |
| parse-result | Marimay VM (source run) | 0.79 | 1.43 | 133.63–143.69 | 2% |
| parse-result | Bun / TypeScript | 0.13 | 1.08 | 12.53–15.72 | 8% |
| insertion | Marimay native | 0.41 | 1.94 | 47.27–52.90 | 4% |
| insertion | Go native | 0.27 | 1.43 | 28.96–31.21 | 5% |
| insertion | Rust native | 0.61 | 1.35 | 28.16–31.04 | 6% |
| insertion | Marimay VM (source run) | 82.88 | 130.47 | 5992.79–6299.94 | 4% |
| insertion | Bun / TypeScript | 0.33 | 1.61 | 79.49–82.47 | 2% |
| heap-sort | Marimay native | 0.30 | 0.60 | 31.81–37.46 | 3% |
| heap-sort | Go native | 0.21 | 0.42 | 38.88–43.83 | 2% |
| heap-sort | Rust native | 0.78 | 2.46 | 21.90–25.05 | 11% |
| heap-sort | Marimay VM (source run) | 3.80 | 12.99 | 1672.79–1796.69 | 2% |
| heap-sort | Bun / TypeScript | 0.99 | 4.80 | 90.56–106.02 | 5% |
| stack | Marimay native | 0.09 | 0.24 | 9.65–12.23 | 3% |
| stack | Go native | 0.23 | 0.50 | 14.05–16.50 | 5% |
| stack | Rust native | 0.10 | 0.22 | 8.75–10.41 | 3% |
| stack | Marimay VM (source run) | 3.36 | 18.03 | 1034.72–1139.04 | 2% |
| stack | Bun / TypeScript | 0.48 | 1.23 | 21.04–25.18 | 7% |
| queue | Marimay native | 0.17 | 0.48 | 9.87–11.86 | 5% |
| queue | Go native | 0.19 | 0.71 | 14.34–15.54 | 5% |
| queue | Rust native | 0.10 | 0.20 | 8.82–10.70 | 3% |
| queue | Marimay VM (source run) | 5.27 | 14.77 | 1139.18–1273.63 | 2% |
| queue | Bun / TypeScript | 0.31 | 1.36 | 25.17–29.19 | 5% |
| min-heap | Marimay native | 0.28 | 0.72 | 45.76–65.50 | 2% |
| min-heap | Go native | 0.41 | 0.82 | 53.05–71.92 | 2% |
| min-heap | Rust native | 0.69 | 1.01 | 28.85–49.82 | 7% |
| min-heap | Marimay VM (source run) | 48.77 | 166.01 | 5616.28–6333.11 | 3% |
| min-heap | Bun / TypeScript | 0.77 | 3.09 | 106.16–180.42 | 3% |
| dsu | Marimay native | 0.45 | 2.16 | 29.49–34.73 | 7% |
| dsu | Go native | 0.17 | 0.35 | 24.08–28.59 | 2% |
| dsu | Rust native | 0.70 | 1.96 | 21.50–24.36 | 9% |
| dsu | Marimay VM (source run) | 26.48 | 145.44 | 5410.07–6327.47 | 3% |
| dsu | Bun / TypeScript | 1.00 | 3.65 | 47.25–71.15 | 7% |
| bfs | Marimay native | 0.42 | 1.58 | 65.41–77.38 | 2% |
| bfs | Go native | 0.86 | 2.09 | 58.92–64.43 | 4% |
| bfs | Rust native | 0.17 | 0.57 | 23.35–25.32 | 2% |
| bfs | Marimay VM (source run) | 10.17 | 20.69 | 5501.93–5666.21 | 2% |
| bfs | Bun / TypeScript | 0.26 | 1.18 | 67.33–70.63 | 2% |
| dijkstra | Marimay native | 0.28 | 0.62 | 40.98–42.65 | 2% |
| dijkstra | Go native | 0.18 | 0.42 | 40.73–41.39 | 2% |
| dijkstra | Rust native | 0.13 | 1.21 | 38.91–40.29 | 3% |
| dijkstra | Marimay VM (source run) | 4.05 | 18.89 | 2394.77–2523.80 | 2% |
| dijkstra | Bun / TypeScript | 0.83 | 1.80 | 74.40–77.26 | 3% |
| frequency-map | Marimay native | 0.30 | 0.40 | 32.17–35.18 | 3% |
| frequency-map | Go native | 0.17 | 0.31 | 13.76–15.30 | 4% |
| frequency-map | Rust native | 1.46 | 9.03 | 15.28–25.26 | 38% |
| frequency-map | Marimay VM (source run) | 0.44 | 3.13 | 474.30–512.87 | 2% |
| frequency-map | Bun / TypeScript | 0.36 | 0.94 | 26.79–31.68 | 4% |
| unique-set | Marimay native | 0.22 | 0.54 | 26.68–29.11 | 2% |
| unique-set | Go native | 0.20 | 0.39 | 15.85–17.48 | 4% |
| unique-set | Rust native | 0.21 | 0.82 | 18.44–20.86 | 4% |
| unique-set | Marimay VM (source run) | 2.23 | 12.14 | 348.50–492.93 | 3% |
| unique-set | Bun / TypeScript | 0.45 | 1.04 | 20.98–25.13 | 6% |
| rune-frequency | Marimay native | 0.15 | 0.30 | 22.33–24.05 | 2% |
| rune-frequency | Go native | 0.22 | 0.41 | 5.56–6.33 | 11% |
| rune-frequency | Rust native | 0.33 | 0.88 | 5.89–7.06 | 16% |
| rune-frequency | Marimay VM (source run) | 0.54 | 1.00 | 248.17–258.36 | 2% |
| rune-frequency | Bun / TypeScript | 0.43 | 1.11 | 16.01–18.34 | 8% |

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
- **insertion**: 50 × 2,500 generated integers
- **heap-sort**: 5 × 100,000 generated integers
- **stack**: 1,000,000 push + pop
- **queue**: 1,000,000 enqueue + dequeue
- **min-heap**: 500,000 insert + remove-min
- **dsu**: 100,000 nodes; 5,000,000 unions
- **bfs**: 300 × 20,000 nodes, degree 4
- **dijkstra**: 80 × 800 nodes, O(V²)
- **frequency-map**: 1,000,000 integers; 4,096-key histogram
- **unique-set**: 1,000,000 integers; distinct-value count
- **rune-frequency**: 450,000 Unicode scalars; 12-key histogram

## Interpretation limits

- No general Unicode lower/casefold API: normalize-title measures a shared corpus folding helper only.
- No I/O, concurrency, JSON or HTTP claims.
- Allocation workloads prescribe escaping objects; allocation counts, GC pauses and peak RSS are not measured.
- Map/set implementations retain host ordering, hashing, growth and GC policies. Cross-language equality is observable results, not identical runtime layouts.
- Go uses *Book and Rust Rc<Book> to preserve Marimay reference identity; Rust Rc costs do not generalize to all Rust representations.
- BFS has fixed degree 16 and contiguous IDs; it is not an O(V²)-edge dense graph and record edges are IDs, not object pointers.
- Bun uses JavaScript numbers for bounded exact integers, UTF-16 strings with UTF-8 byte checksums, Map/Set and reference objects; storage and copying are runtime-controlled.
- Bun report-builder uses an array of chunks plus join; concatenation may use ropes. Split and scalar strings are independently retainable values, without a forced physical copy in JavaScript.
- TypeScript interfaces are erased; catalog-interface measures a materialized structural-interface array and an ordinary method call, not a guaranteed vtable dispatch.
- JavaScript has no reserve-only Array API: array-reserved uses new Array(n) plus indexed writes; array-grow uses push. These are equivalent values, not identical allocation/append traces.
- The per-workload Go targets are exploratory thresholds, not reviewed release budgets. No average score or general ‘Go parity’ verdict is computed.
- Short cases can be dominated by process startup and validation; repeat with larger documented inputs before attributing a difference to dispatch, GC or a particular primitive.
- Interface results include array construction/boxing and compiler devirtualization opportunities; they are not isolated virtual-call latency.

## Toolchains

- python: `3.9.6`
- marimay: `Marimay compiler 0.1.0-alpha.1`
- go: `go version go1.26.4 darwin/arm64`
- rust: `rustc 1.96.0 (ac68faa20 2026-05-25)`
- bun: `1.4.2`

Command: `./benchmarks/catalog_bench.py --anchors --output benchmarks/results/comprehensive-local.md`
