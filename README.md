# Algorithms in Marimay, Go, and Rust

Учебный репозиторий с одинаковым набором алгоритмов на трёх языках. Его цель —
не найти самый короткий синтаксис, а сравнить модели данных, обработку
отсутствующих значений, package boundaries, мутацию и зрелость toolchain.

## Состав

```text
algorithm-benchmarks/
  marimay/
    mmay.mod
    sorting/{insertion,heap}.my
    structures/{stack,queue,heap,dsu}.my
    graphs/{bfs,dijkstra}.my
    counting/counting.my
    benchmarks/{core,...,frequency_map,unique_set,rune_frequency}/
    probes/{core,scalar_get,scalar_set,proven_bounds,unproven_bounds,growth,reserved_growth,density,nested_traversal,checked_loop}/
    features/{core,dynamic_text}/
    algorithms_test.my
  go/
    counting/
    sorting/
    structures/
    graphs/
    algorithms_test.go
  rust/
    src/{counting,sorting,structures,graphs}/
    tests/algorithms_test.rs
  typescript/src/{sorting,structures,graphs,benchmark}.ts
  v/{sorting,structures,graphs,cmd/benchmark}/
  moonbit/{sorting,structures,graphs,cmd/benchmark}/
  benchmarks/{run.py,probes.py,feature_probes.py,validate_results.py,results/,budgets/}
  verify.sh
```

Реализованы:

- insertion sort и heap sort;
- stack, FIFO queue, binary min-heap и disjoint-set union;
- BFS с расстояниями от начальной вершины;
- Dijkstra для неотрицательных весов;
- integer frequency map, set-based distinct count и Unicode rune frequency map.

Во всех трёх версиях Dijkstra намеренно использует одинаковый учебный вариант
`O(V²)`, чтобы сравнение не зависело от библиотечной priority queue.

## Полная проверка

Corpus зафиксирован на Marimay `0.1.0-alpha.1` с языковым контрактом
`0.1-design`. Точные версии compiler/runtime/standard library и обязательные
команды находятся в `benchmarks/marimay-toolchain.json`; verification и все
benchmark harness отклоняют несовместимый `mmay` до сборки и измерений.

По умолчанию скрипт ищет Marimay в соседнем репозитории
`../marimay/build/debug/mmay`:

```sh
./verify.sh
```

Для другого бинарника:

```sh
MMAY=/absolute/path/to/mmay ./verify.sh
```

Или через Make:

```sh
make verify
```

Скрипт выполняет:

- Marimay: canonical format check и `mmay check` для библиотек и benchmark-кода,
  VM run, пять explicit tests через `--engine both`, Debug/Release native
  build, отдельный native `dynamic-text` checksum и побайтовое сравнение stdout;
- Go: `gofmt`, `go vet`, `go test ./...`, `go run .`;
- Rust: `cargo fmt --check`, strict Clippy, все tests и запуск основного binary.
- Общий machine-readable
  [`equivalence.json`](benchmarks/equivalence.json): схема, LCG, размеры,
  операции, representation, checks и checksum каждого workload; валидатор и
  его негативные unit-тесты блокируют дрейф entrypoint'ов и возврат inline
  обходов.

## Сравнительный benchmark

```sh
make benchmark
```

Он заранее собирает release native executable через `mmay build --release`,
`go build` и `cargo build --release`, а затем запускает одинаковые
детерминированные нагрузки. Время компиляции исключено; `mmay run`/VM не
смешивается с native-результатами. Совпадение checksum обязательно для каждого
языка и каждого замера.

Перед сборкой harness проверяет
[`equivalence.json`](benchmarks/equivalence.json) и берёт из него список
workload, описания и ожидаемые checksum. Источник Marimay compiler, revision
corpus и SHA-256 manifest записываются в Markdown и raw JSON отчёты.

Три алгоритма на новых `Map`, `Set` и `rune` запускаются вместе с восемью
историческими workload отдельной локальной матрицей:

```sh
MMAY=/absolute/path/to/release/mmay make benchmark-expanded
```

Команда читает [`expanded_workloads.json`](benchmarks/expanded_workloads.json),
сравнивает Marimay, Go и Rust и пишет `expanded-algorithms-local.{md,json}`.
Расширенный отчёт не меняет опубликованные checkpoint-21 baseline и их SHA.

Для локального расширенного сравнения доступны TypeScript под Bun, V и MoonBit:

```sh
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/run.py \
  --languages marimay,go,rust,typescript,v,moonbit \
  --samples 11 --warmups 3 \
  --output benchmarks/results/local-six-languages.md
```

Harness принимает `BUN`, `V` и `MOON` как пути к исполняемым файлам. TypeScript
заранее компилируется через `bun build --compile --minify`, V — через `v -prod`,
MoonBit — через `moon build --release --target native`; компиляция не входит в
замеры. Эти toolchain не устанавливаются и не запускаются в `verify.sh` или CI.
Расширенный JSON помечается `comparison_scope: local-only`, использует отдельный
[`local_participants.json`](benchmarks/local_participants.json) и запрещён как
Tier 1 baseline. Штатный `make benchmark` по-прежнему измеряет только
`marimay,go,rust`.

Новые языковые возможности измеряются отдельным `make benchmark-features`.
Feature-probes используют release runtime и сохраняют raw samples, но остаются
local-only и не меняют исторические array/native budgets без review.
Push в `main` запускает Linux x86_64 runner: он повторяет 9 focused probes и 8
canonical algorithms против reviewed checkpoint-21 ceilings, отдельно собирает
`dynamic-text` candidate и публикует все raw samples в evidence branch.

Воспроизводимый checkpoint-21 baseline, focused array probes, raw samples,
artifact hashes и reviewed macOS arm64 budget находятся в
[`benchmarks/results/`](benchmarks/results/) и
[`benchmarks/budgets/`](benchmarks/budgets/). Методика, schema, retry и
validation commands: [`benchmarks/README.md`](benchmarks/README.md).

Развёрнутые выводы и места оптимизации зафиксированы в основном Marimay-репозитории:
[`algorithm-benchmark-findings.md`](../marimay/docs/research/algorithm-benchmark-findings.md).
Предложение по `[][]int` и соседние ergonomics-наблюдения вынесены отдельно:
[`array-type-shorthand-proposal.md`](../marimay/docs/design/array-type-shorthand-proposal.md).

## Общие контрольные примеры

| Семейство | Вход | Ожидаемый результат |
|---|---|---|
| insertion sort | `[5, -1, 5, 3, 0]` | `[-1, 0, 3, 5, 5]` |
| heap sort | `[9, 4, 7, 1, -2, 6, 5]` | `[-2, 1, 4, 5, 6, 7, 9]` |
| stack | `10, 20, 30` | первый pop возвращает `30` |
| queue | `10, 20, 30` | первый dequeue возвращает `10` |
| min-heap | `7, 2, 9, 1, 5` | первый pop возвращает `1` |
| DSU | union `(0,1)`, `(1,2)`, `(3,4)` | `0~2`, но не `0~3`; 3 компоненты |
| BFS | пятивершинный неориентированный граф | `[0, 1, 1, 2, 2]` |
| Dijkstra | пятивершинный ориентированный граф | `[0, 3, 1, 4, 7]` |
| frequency map | `2, 1, 2, -4, 1, 2` | частота `2` равна `3` |
| unique set | `2, 1, 2, -4, 1, 2` | `3` различных значения |
| rune frequency | `λλ🚀` | `2` различных rune; частота `λ` равна `2` |

## Текущее состояние Marimay 0.1.0-alpha.1

Это наблюдения о текущем Stage 0, а не предложения менять спецификацию языка.

1. После checkpoints 14–18 Marimay root, correctness tests и timed entrypoints
   вызывают одни reusable sorting/structures/graphs/counting packages. Cross-package
   `[]T`, imported generic results, receiver-directed `push`/`pop`/`length`,
   physical array `pop` и canonical `[][]T` проверяются VM и native engines.
2. Stack и min-heap больше не хранят shadow logical size: они используют
   обычные package-owned `push`/`pop` поверх managed arrays. BFS/Dijkstra
   возвращают `Option<[]int>`, а Dijkstra использует `[][]Edge`, как Go/Rust
   используют nested edge records.
3. Stack/queue workload по пять миллионов добавлений и извлечений достигал
   текущего native resource limit (`I0002`). Для общего benchmark используется
   один миллион; это ограничение отдельно зафиксировано в методике.
4. Checkpoints 14–18 закрывают correctness/ergonomics, а не основные hot-path
   optimization. Bounds facts и native access boundary закрыты в checkpoints
   22–23; dense storage, capacity planning, nested traversal audit и
   checked-integer proof pipeline относятся к checkpoints 24–27, а reusable
   corpus остаётся public integration gate checkpoint 28.
5. Correctness suites всех трёх языков отдельно отклоняют out-of-range graph
   starts/endpoints и negative Dijkstra weights. Эти probes не входят в timed
   interval; Rust использует `usize` для индексов, поэтому отрицательный индекс
   там не представим, а не принимается.

Checkpoint-21 budget блокирует workload-local регрессии на конкретном
зарегистрированном runner; он не превращает локальные цифры в обещание общей
скорости языка или cross-language ranking.
