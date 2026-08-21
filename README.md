# Algorithms in Ruda, Go, and Rust

Учебный репозиторий с одинаковым набором алгоритмов на трёх языках. Его цель —
не найти самый короткий синтаксис, а сравнить модели данных, обработку
отсутствующих значений, package boundaries, мутацию и зрелость toolchain.

## Состав

```text
ruda-algotithms/
  ruda/
    ruda.mod
    sorting/{insertion,heap}.ruda
    structures/{stack,queue,heap,dsu}.ruda
    graphs/{bfs,dijkstra}.ruda
    benchmarks/{core,insertion,heap_sort,stack,queue,min_heap,dsu,bfs,dijkstra}/
    probes/{core,scalar_get,scalar_set,proven_bounds,unproven_bounds,growth,reserved_growth,density,nested_traversal,checked_loop}/
    algorithms_test.ruda
  go/
    sorting/
    structures/
    graphs/
    algorithms_test.go
  rust/
    src/{sorting,structures,graphs}/
    tests/algorithms_test.rs
  benchmarks/{run.py,probes.py,validate_results.py,results/,budgets/}
  verify.sh
```

Реализованы:

- insertion sort и heap sort;
- stack, FIFO queue, binary min-heap и disjoint-set union;
- BFS с расстояниями от начальной вершины;
- Dijkstra для неотрицательных весов.

Во всех трёх версиях Dijkstra намеренно использует одинаковый учебный вариант
`O(V²)`, чтобы сравнение не зависело от библиотечной priority queue.

## Полная проверка

По умолчанию скрипт ищет Ruda в соседнем репозитории
`../Ma/build/debug/ruda`:

```sh
./verify.sh
```

Для другого бинарника:

```sh
RUDA=/absolute/path/to/ruda ./verify.sh
```

Или через Make:

```sh
make verify
```

Скрипт выполняет:

- Ruda: canonical format check и `ruda check` для библиотек и benchmark-кода,
  VM run, четыре explicit tests через `--engine both`, Debug/Release native
  build и побайтовое сравнение stdout всех трёх исполнений;
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

Он заранее собирает release native executable через `ruda build --release`,
`go build` и `cargo build --release`, а затем запускает одинаковые
детерминированные нагрузки. Время компиляции исключено; `ruda run`/VM не
смешивается с native-результатами. Совпадение checksum обязательно для каждого
языка и каждого замера.

Перед сборкой harness проверяет
[`equivalence.json`](benchmarks/equivalence.json) и берёт из него список
workload, описания и ожидаемые checksum. Источник Ruda compiler, revision
corpus и SHA-256 manifest записываются в Markdown и raw JSON отчёты.

Воспроизводимый checkpoint-21 baseline, focused array probes, raw samples,
artifact hashes и reviewed macOS arm64 budget находятся в
[`benchmarks/results/`](benchmarks/results/) и
[`benchmarks/budgets/`](benchmarks/budgets/). Методика, schema, retry и
validation commands: [`benchmarks/README.md`](benchmarks/README.md).

Развёрнутые выводы и места оптимизации зафиксированы в основном Ruda-репозитории:
[`algorithm-benchmark-findings.md`](../Ma/docs/research/algorithm-benchmark-findings.md).
Предложение по `[][]int` и соседние ergonomics-наблюдения вынесены отдельно:
[`array-type-shorthand-proposal.md`](../Ma/docs/design/array-type-shorthand-proposal.md).

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

## Текущее состояние Ruda 0.1-dev

Это наблюдения о текущем Stage 0, а не предложения менять спецификацию языка.

1. После checkpoints 14–18 Ruda root, correctness tests и timed entrypoints
   вызывают одни reusable sorting/structures/graphs packages. Cross-package
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
   optimization. Bounds facts, native access boundary, dense scalar storage,
   capacity planning и nested traversal запланированы checkpoints 22–27.
5. Correctness suites всех трёх языков отдельно отклоняют out-of-range graph
   starts/endpoints и negative Dijkstra weights. Эти probes не входят в timed
   interval; Rust использует `usize` для индексов, поэтому отрицательный индекс
   там не представим, а не принимается.

Checkpoint-21 budget блокирует workload-local регрессии на конкретном
зарегистрированном runner; он не превращает локальные цифры в обещание общей
скорости языка или cross-language ranking.
