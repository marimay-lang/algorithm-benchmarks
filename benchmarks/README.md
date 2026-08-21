# Benchmark methodology

`run.py` сравнивает восемь одинаковых детерминированных workload в Ruda, Go и
Rust. Для Ruda он вызывает `ruda build --release`, а затем измеряет полученный
native executable напрямую — `ruda run` и VM в эту таблицу не входят.
Компиляция всех трёх языков выполняется заранее и в результаты не входит.

Machine-readable contract находится в
[`equivalence.json`](equivalence.json). Он фиксирует LCG, checksum, размеры,
операции, representation, selected checks и reusable entrypoint markers.
[`validate_equivalence.py`](validate_equivalence.py) проверяет contract и
исходники до любой сборки; `run.py` получает из manifest список workload,
описания и ожидаемые checksum вместо отдельной таблицы констант.

```sh
./benchmarks/run.py
```

Полезные параметры:

```sh
./benchmarks/run.py --samples 11 --warmups 3
./benchmarks/run.py --skip-build
./benchmarks/run.py --languages go,rust
RUDA=/absolute/path/to/ruda ./benchmarks/run.py
```

По умолчанию используется `../Ma/build/release/ruda`. После checkpoint 13
requested output profile сам выбирает согласованный release runtime независимо
от build profile compiler executable; release-путь сохраняется как единая
локальная convention. Путь к реально использованному compiler executable
записывается в каждом отчёте.

## Что измеряется

- release/optimized native executable каждого языка;
- одинаковый LCG: `state = (state * 25173 + 13849) % 65536`;
- одинаковые размеры, повторы и алгоритмы;
- wall-clock от запуска процесса до завершения;
- median по умолчанию из 3 запусков после одного warmup;
- min/max сохраняются вместе со всеми сырыми измерениями.

Каждый процесс печатает `<benchmark> <checksum>`. Harness отклоняет запуск,
если checksum отличается хотя бы в одном языке. Порядок языков вращается между
образцами, чтобы постоянный первый/последний участник не получал систематическое
преимущество.

Correctness suites дополнительно проверяют одинаковое отклонение out-of-range
starts/endpoints и отрицательных весов Dijkstra. Эти invalid-input probes не
включены в timing. Rust graph indices имеют тип `usize`, поэтому signed
negative index там исключён representation, что явно записано в manifest.

Время включает process startup, инициализацию входа и одну строку stdout. Оно
не включает компиляцию. Вход создаётся внутри измеряемого процесса, потому что
текущий Ruda preview не имеет подходящего стабильного binary-input API.

Изначально stack и queue нагружались пятью миллионами операций, но текущий
Ruda native runtime завершал такие процессы с `error[I0002]: native runtime
resource limit reached`. Поэтому общий успешно исполняемый workload для них —
один миллион добавлений и один миллион извлечений. Это отдельная найденная
граница текущей реализации, а не попытка скрыть её меньшим тестом.

Последние результаты находятся в [`results/latest.md`](results/latest.md), а
сырые времена каждого запуска — в [`results/latest.json`](results/latest.json).
Одноразовый checkpoint-20 checksum/fidelity smoke хранится отдельно в
[`results/cp20-fidelity-smoke.md`](results/cp20-fidelity-smoke.md) и
[`results/cp20-fidelity-smoke.json`](results/cp20-fidelity-smoke.json); один
sample не является performance baseline или budget.

## Ограничения сопоставимости

Одинаковые checksum подтверждают выбранные результаты, но не доказывают
идентичность сгенерированного кода. После checkpoints 14–18 все три языка
вызывают reusable sorting/structures/graphs packages. Stack, queue, min-heap и
DSU выполняют одинаковые операции; BFS использует nested integer arrays;
Dijkstra — nested edge records и учебный `O(V²)` поиск. Ruda/Rust возвращают
`Option`, Go — эквивалентную пару value/bool.

Таблица выявляет крупные расходы текущего runtime/lowering, но не является
стабильным performance gate до Tier 1 protocol и baseline checkpoint 21.

Это практический локальный ориентир, а не доказательство общей скорости языка:
результаты зависят от CPU, температуры, фоновой нагрузки, версий toolchain и
конкретных реализаций. Для исследования генератора C можно отдельно сравнивать
emitted C и compiler flags, не смешивая это с таблицей пользовательских
workload.
