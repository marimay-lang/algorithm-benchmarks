# Benchmark methodology

`run.py` сравнивает восемь одинаковых детерминированных workload в Ruda, Go и
Rust. `probes.py` отдельно измеряет девять focused Ruda workload, которые
разделяют стоимость scalar get/set, доказуемых и динамических bounds,
growth/reserve, плотного scalar storage, nested traversal и checked integer
loops. Для Ruda оба harness вызывают `ruda build --release` с фиксированным
managed-heap budget, а затем измеряют native executable напрямую. Компиляция и
`ruda run`/VM в эти результаты не входят.

Machine-readable workload contract находится в
[`equivalence.json`](equivalence.json). Он фиксирует LCG, checksum, размеры,
операции, representation, selected checks и reusable entrypoint markers.
[`validate_equivalence.py`](validate_equivalence.py) проверяет contract и
исходники до любой сборки; `run.py` не владеет вторым списком констант.

Checkpoint-21 measurement contract находится в
[`performance_protocol.json`](performance_protocol.json). Он фиксирует
release profile, 3 warmup и не менее 11 нечётных measured samples,
300-секундный per-process timeout, сбалансированную ротацию workload/language,
`perf_counter_ns`, median, MAD, Tukey IQR, noise envelope, 64 MiB heap budget и
правило ровно одного полного retry после cool-down. [`probes.json`](probes.json)
владеет probe IDs, cost categories, entrypoints и checksum.

## Tier 1 commands

```sh
RUDA=/absolute/path/to/release/ruda \
  ./benchmarks/probes.py --samples 11 --warmups 3 \
  --output benchmarks/results/cp21-probes-PLATFORM.json
RUDA=/absolute/path/to/release/ruda \
  ./benchmarks/run.py --languages ruda,go,rust --samples 11 --warmups 3 \
  --output benchmarks/results/cp21-algorithms-PLATFORM.md
./benchmarks/validate_results.py \
  benchmarks/results/cp21-probes-PLATFORM.json \
  benchmarks/results/cp21-algorithms-PLATFORM.json
```

После review каждого platform budget он добавляется в
[`tier1-baselines.json`](tier1-baselines.json). Единственный aggregate completion
gate — `./benchmarks/validate_tier1_baselines.py` (или `make
benchmark-validate`): он требует ровно по одной совместимой baseline для Linux
x86_64, Linux arm64, macOS arm64, macOS x86_64 и Windows x86_64, повторно
проверяет raw schema/current manifests и связывает budget с точными result
paths/SHA-256. Неполный registry намеренно не проходит этот gate; отдельную уже
зарегистрированную платформу можно проверить `make benchmark-validate-platform`.

По умолчанию используется `../Ma/build/release/ruda`. После checkpoint 13
requested output profile выбирает согласованный release runtime независимо от
build profile compiler executable. Harness проверяет release runtime manifest,
а не полагается на имя compiler path.

`--skip-build` допустим только для немедленного локального повтора уже
проверенных artifacts. Published baseline command всегда сначала собирает
исполняемые файлы. Tier 1 algorithm report содержит полный `ruda,go,rust`
набор в protocol order; частичная language matrix не принимается этой схемой.

## Что измеряется

- release/optimized native executable каждого языка;
- одинаковый LCG: `state = (state * 25173 + 13849) % 65536`;
- одинаковые размеры, повторы и reusable algorithms;
- wall-clock от запуска процесса до завершения;
- median из не менее 11 запусков после не менее 3 warmup;
- MAD, IQR, min/max, noise fraction, каждый raw sample и фактический порядок.

Каждый процесс печатает ровно `<benchmark> <checksum>\n` без stderr. Harness
отклоняет другой checksum, байты, exit status или timeout. Порядок workload и
языков вращается между раундами, чтобы постоянный первый/последний участник не
получал систематического преимущества. Время включает process startup,
инициализацию входа и одну строку stdout; вход создаётся внутри процесса.

Correctness suites отдельно проверяют отклонение out-of-range graph
starts/endpoints и отрицательных весов Dijkstra. Эти invalid-input probes не
включены в timing. Rust graph indices имеют тип `usize`, поэтому signed
negative index там исключён representation, что записано в manifest.

## Isolation, metadata и budgets

Перед baseline оператор выделяет runner без параллельных repository jobs,
фиксирует power policy, отключает automatic sleep на интервал и не выбирает
«лучшие» samples. JSON сохраняет platform/CPU/load/power metadata, полные
toolchain versions, command, compiler/runtime paths и SHA-256, runtime
manifest/profile, generated-C compiler/linker versions/flags, corpus/manifest
revisions и resource budget.

Валидатор отклоняет debug runtime, неполные metadata, NaN/Infinity,
недостаточные samples, несовместимую baseline и дрейф checksum/source manifest.
Порог — не cross-language ratio. Для каждого Ruda workload и platform он равен
`baseline median × (1 + max(10%, noise envelope))`, где envelope — максимум из
2%, `3 × MAD / median` и `IQR / median`.

Превышение требует одного полного повторного 11/3 запуска после cool-down;
release regression подтверждается, только если обе независимые медианы выше
того же reviewed budget. Automatic retry не превращает flaky failure в pass,
и оба raw report сохраняются.

## Results

Checkpoint-21 macOS arm64/Apple M2 baseline находится в
[`results/cp21-algorithms-macos-arm64-apple-m2.md`](results/cp21-algorithms-macos-arm64-apple-m2.md),
[`results/cp21-algorithms-macos-arm64-apple-m2.json`](results/cp21-algorithms-macos-arm64-apple-m2.json)
и [`results/cp21-probes-macos-arm64-apple-m2.json`](results/cp21-probes-macos-arm64-apple-m2.json).
Reviewed thresholds находятся в
[`budgets/cp21-macos-arm64-apple-m2.json`](budgets/cp21-macos-arm64-apple-m2.json).
Registry пока содержит только доступную macOS arm64 baseline; aggregate Tier 1
gate перечисляет отсутствующие платформы и остаётся красным до их измерения и
review.

Legacy `results/latest.*`, debug-runtime baseline и checkpoint-20 smoke —
historical local evidence; они не проходят checkpoint-21 schema. Именованные
raw reports вместе с совместимым reviewed platform budget образуют regression
gate. Cross-language ranking и универсальные speed claims остаются вне scope.
