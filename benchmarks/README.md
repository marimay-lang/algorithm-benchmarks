# Benchmark methodology

`run.py` по умолчанию сравнивает восемь одинаковых детерминированных workload в
Marimay, Go и Rust. С `--expanded` он добавляет три local-only workload для
`Map`, `Set` и Unicode `rune`, описанные в
[`expanded_workloads.json`](expanded_workloads.json). `probes.py` отдельно
измеряет девять focused Marimay workload, которые
разделяют стоимость scalar get/set, доказуемых и динамических bounds,
growth/reserve, плотного scalar storage, nested traversal и checked integer
loops. Для Marimay оба harness вызывают `mmay build --release` с фиксированным
managed-heap budget, а затем измеряют native executable напрямую. Компиляция и
`mmay run`/VM в эти результаты не входят.

Machine-readable workload contract находится в
[`equivalence.json`](equivalence.json). Он фиксирует LCG, checksum, размеры,
операции, representation, selected checks и reusable entrypoint markers.
[`validate_equivalence.py`](validate_equivalence.py) проверяет contract и
исходники до любой сборки; `run.py` не владеет вторым списком констант.
Совместимый Marimay toolchain отдельно закреплён в
[`marimay-toolchain.json`](marimay-toolchain.json): все harness проверяют
machine-readable `mmay version --json` до создания benchmark artifacts.

Расширенная локальная матрица запускается так:

```sh
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/run.py --expanded --samples 11 --warmups 3 \
  --output benchmarks/results/expanded-algorithms-local.md
```

Она включает все одиннадцать алгоритмов на Marimay, Go и Rust, использует тот
же measurement protocol и checksum gate, но помечается `local-only`. Поэтому
новые нагрузки не переписывают исторический eight-workload manifest и не могут
случайно стать частью checkpoint-21 budget.

Checkpoint-21 measurement contract находится в
[`performance_protocol.json`](performance_protocol.json). Он фиксирует
release profile, 3 warmup и не менее 11 нечётных measured samples,
300-секундный per-process timeout, сбалансированную ротацию workload/language,
`perf_counter_ns`, median, MAD, Tukey IQR, noise envelope, 64 MiB heap budget и
правило ровно одного полного retry после cool-down. [`probes.json`](probes.json)
владеет probe IDs, cost categories, entrypoints и checksum.

## Checkpoint 21 and public-alpha commands

```sh
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/probes.py --samples 11 --warmups 3 \
  --output benchmarks/results/cp21-probes-PLATFORM.json
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/run.py --languages marimay,go,rust --samples 11 --warmups 3 \
  --output benchmarks/results/cp21-algorithms-PLATFORM.md
./benchmarks/validate_results.py \
  benchmarks/results/cp21-probes-PLATFORM.json \
  benchmarks/results/cp21-algorithms-PLATFORM.json
```

После review каждого platform budget он добавляется в
[`tier1-baselines.json`](tier1-baselines.json). `make benchmark-validate`
закрывает checkpoint 21 по dedicated Linux x86_64 runner: он повторно проверяет
raw schema/current manifests и связывает reviewed budget с точными result
paths/SHA-256. `make benchmark-validate-public-alpha` сохраняет отдельный
отложенный gate и требует по одной совместимой baseline для Linux x86_64,
Linux arm64, macOS arm64, macOS x86_64 и Windows x86_64. Поэтому завершение
checkpoint 21 не выдаётся за полную Tier 1 готовность публичной альфы. Linux
baseline отдельно проверяется `make benchmark-validate-platform`.

По умолчанию используется `../marimay/build/release/mmay`. После checkpoint 13
requested output profile выбирает согласованный release runtime независимо от
build profile compiler executable. Harness проверяет release runtime manifest,
а не полагается на имя compiler path.

`--skip-build` допустим только для немедленного локального повтора уже
проверенных artifacts. Published baseline command всегда сначала собирает
исполняемые файлы. Tier 1 algorithm report содержит полный `marimay,go,rust`
набор в protocol order. Focused checkpoint report может выбрать ordered subset
через `--languages` и помечается `measurement_scope=focused`; он сравнивается
только как candidate и не может стать reviewed Tier 1 baseline.

После checkpoint 24 focused performance gates могут собирать только нужную
группу probes, не меняя measurement protocol:

```sh
./benchmarks/probes.py --probe capacity --output benchmarks/results/cp25-capacity-PLATFORM.json
./benchmarks/probes.py --probe nested-traversal --output benchmarks/results/cp26-nested-PLATFORM.json
./benchmarks/probes.py --probe checked-integer --output benchmarks/results/cp27-integer-PLATFORM.json
./benchmarks/validate_results.py benchmarks/results/cp25-capacity-PLATFORM.json
```

`capacity` выбирает `growth` и `reserved-growth`; `nested-traversal` и
`checked-integer` выбирают одноимённый nested probe и `checked-loop`.
Валидатор принимает полный или focused candidate и сравнивает присутствующие
workload с reviewed platform ceilings. Строгая привязка exact paths/SHA-256
сохраняется для самих checkpoint-21 baseline. `--baseline` принимает
исторический algorithm report того же platform/workload set как comparison
context, но не подменяет reviewed budget.

## Local-only language feature probes

Новые языковые возможности измеряются отдельно от исторического array/native
manifest, чтобы не менять его source hashes и reviewed budgets. Feature-probe
использует тот же release profile, 64 MiB managed heap, 3 warmup + 11 samples,
raw timings и noise statistics, но имеет отдельную schema и всегда помечен
`comparison_scope=local-only`:

```sh
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/feature_probes.py --feature dynamic-text \
  --output benchmarks/results/cp30-dynamic-text-local.json
```

`dynamic-text` измеряет интерполяцию, форматирование `int`/`bool`, сборку строк
и `parseInt` в одном детерминированном цикле. Первый отчёт является candidate,
а не reviewed budget; публиковать threshold можно только отдельным решением и
повторяемым baseline по D056.

Workflow `cp21-baseline.yml` сохраняет историческое имя файла, но на каждом
push в `main` выполняет текущую CP30 regression matrix на Linux x86_64. Он
проверяет 9 probes и 8 algorithms против reviewed checkpoint-21 ceilings,
собирает отдельный `cp30-dynamic-text-linux-x86_64.json` без автоматического
threshold и публикует raw evidence в `evidence/cp30-linux-x86_64-<revision>`.

## Локальные дополнительные языки

TypeScript/Bun, V и MoonBit подключаются только явным расширением canonical
матрицы:

```sh
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/run.py \
  --languages marimay,go,rust,typescript,v,moonbit \
  --samples 11 --warmups 3 \
  --output benchmarks/results/local-six-languages.md
```

Пути к локальным toolchain можно задать переменными `BUN`, `V` и `MOON`.
TypeScript собирается Bun в standalone executable, V — production native
executable, MoonBit — release native executable. Отдельный
[`local_participants.json`](local_participants.json) связывает их исходники,
workload IDs и checksum с canonical [`equivalence.json`](equivalence.json), не
меняя hash исторических Tier 1 baseline.

Расширенный result всегда содержит `comparison_scope: local-only` и не может
использоваться `validate_results.py`, reviewed budget или Tier 1 registry.
`verify.sh` проверяет manifest, source contracts и негативные protocol tests,
но не требует и не устанавливает Bun, V или MoonBit. Поэтому стандартный CI и
`make benchmark` остаются на `marimay,go,rust`.

## Что измеряется

- release/optimized native executable каждого языка;
- одинаковый LCG: `state = (state * 25173 + 13849) % 65536`;
- одинаковые размеры, повторы и reusable algorithms;
- для expanded workload одинаковые hash-map/hash-set representations и
  одинаковая последовательность Unicode scalar values;
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
Порог — не cross-language ratio. Для каждого Marimay workload и platform он равен
`baseline median × (1 + max(10%, noise envelope))`, где envelope — максимум из
2%, `3 × MAD / median` и `IQR / median`.

Превышение требует одного полного повторного 11/3 запуска после cool-down;
release regression подтверждается, только если обе независимые медианы выше
того же reviewed budget. Automatic retry не превращает flaky failure в pass,
и оба raw report сохраняются.

## Results

Checkpoint-21 Linux x86_64 baseline находится в
[`results/cp21-algorithms-linux-x86_64.md`](results/cp21-algorithms-linux-x86_64.md),
[`results/cp21-algorithms-linux-x86_64.json`](results/cp21-algorithms-linux-x86_64.json)
и [`results/cp21-probes-linux-x86_64.json`](results/cp21-probes-linux-x86_64.json).
Его reviewed thresholds находятся в
[`budgets/cp21-linux-x86_64.json`](budgets/cp21-linux-x86_64.json).

Ранее собранный дополнительный macOS arm64/Apple M2 baseline находится в
[`results/cp21-algorithms-macos-arm64-apple-m2.md`](results/cp21-algorithms-macos-arm64-apple-m2.md),
[`results/cp21-algorithms-macos-arm64-apple-m2.json`](results/cp21-algorithms-macos-arm64-apple-m2.json)
и [`results/cp21-probes-macos-arm64-apple-m2.json`](results/cp21-probes-macos-arm64-apple-m2.json).
Reviewed thresholds находятся в
[`budgets/cp21-macos-arm64-apple-m2.json`](budgets/cp21-macos-arm64-apple-m2.json).
Он остаётся сохранённым public-alpha evidence, но не расширяет checkpoint-21
completion contract. Public-alpha gate перечисляет отсутствующие Linux arm64,
macOS x86_64 и Windows x86_64 до их измерения и review.

Legacy `results/latest.*`, debug-runtime baseline и checkpoint-20 smoke —
historical local evidence; они не проходят checkpoint-21 schema. Именованные
raw reports вместе с совместимым reviewed platform budget образуют regression
gate. Cross-language ranking и универсальные speed claims остаются вне scope.
