# Catalog and language model: a reproducible comparison

This suite adds 21 application scenarios to 11 algorithm workloads in Marimay,
Go, Rust and TypeScript on Bun. It studies a book-catalog domain; results are
scoped `local-only`, without assigning a language-wide verdict of Go parity.
Historical manifests, the Tier 1 registry and reviewed budgets remain unchanged.

## Run

Run from the `algorithm-benchmarks` root with Go, Rust, Bun and a Release
Marimay compiler. Compiler discovery checks `MMAY`, then `PATH` (the same
`mmay` used by the shell), then the sibling `marimay/build/release/mmay`.
Bun is selected by `BUN=/absolute/path/to/bun` or `PATH`. Missing Bun in the
full matrix is a preparation failure; its column is not silently skipped.

```sh
# Full matrix: 21 application scenarios + 11 algorithm anchors.
MMAY=/absolute/path/to/release/mmay make benchmark-comprehensive

# All 32 scenarios, terminal summary without separate report files.
MMAY=/absolute/path/to/mmay ./benchmarks/catalog_bench.py --anchors --console

# New scenarios including Bun; defaults to 3 warmups + 11 samples.
MMAY=/absolute/path/to/release/mmay make benchmark-catalog

# Quick correctness checks for every new scenario and all five participants.
./benchmarks/catalog_bench.py --profile smoke --verify-only \
  --output benchmarks/results/catalog-smoke-local.md

# Native comparison without VM.
./benchmarks/catalog_bench.py --engine native --samples 11 --warmups 3 \
  --output benchmarks/results/catalog-native-local.md

# Bun / TypeScript only, all 32 scenarios, terminal summary.
./benchmarks/catalog_bench.py --engine bun --anchors --console

# Targeted repeat using the standard inputs, retaining all raw samples.
./benchmarks/catalog_bench.py --workload map-string --workload word-frequency \
  --output benchmarks/results/catalog-text-repeat-local.md

# Validate report integrity, including a report with failed cells.
./benchmarks/catalog_bench.py --validate benchmarks/results/catalog-local.json
```

Every run saves its own copy of the compiler, Release runtime and C headers,
then rebuilds executables in an isolated
`benchmarks/.build/catalog/runs/run-*` directory. Shared Rust outputs are also
copied there before measurement. Bun is copied under its original name `bun`;
metadata records its version and hash. These are ordinary copies, without hard
links, so a system `mmay` update or parallel build cannot replace their contents.
Metadata in the report/journal retains hashes and original paths. If a tool
changes during copying, preparation stops before measurement and requests a retry.

Markdown and JSON reports are written together. The historical suite's
`latest.md/json` are not overwritten. The median summary always appears in the
terminal, including through `make benchmark-comprehensive`. `--console` omits
separate Markdown/JSON reports and cannot be combined with `--output`.

Every observation is immediately written to
`benchmarks/.build/catalog/journals/run-*.jsonl`; the exact path is printed
before measurement. Journals are retained with `--console` too. Journal writes
and integrity checks occur outside the measured interval. Sources, harness,
compiler and executables are checked after each round; compiler/runtime/header
checks use the saved copies. A change stops the run with a nonzero status,
lists changed paths, and marks saved observations diagnostic rather than a
valid comparison. Completed observations also survive Ctrl+C.

During measurement, leave workload sources, harness code and the run directory
unchanged. Updating the original compiler installation after preparation is
safe for the running series, which continues on its saved version.

Inspect saved observations without rerunning:

```sh
./benchmarks/catalog_bench.py --show-journal benchmarks/.build/catalog/journals/run-XXXXXXXX.jsonl
```

Use the path printed by your run. Output identifies diagnostic status and the
sample count in each cell; this does not resume an interrupted series.
`--engine native` selects Marimay native, Go and Rust; `vm` selects only Marimay
VM; `bun` selects only Bun / TypeScript; `both` (default) selects all five.
Older four-participant reports still pass `--validate`. Repeated `--workload`
options select workloads; unknown or duplicate IDs are rejected. `--anchors`
adds all 11 historical algorithms with their fixed inputs, unaffected by the
smoke profile.

`standard` requires at least 3 warmups and 11 odd-numbered samples. `smoke` and
`--verify-only` default to 3 checks per cell without warmup and explicitly
disable parity conclusions. [`catalog_workloads.json`](catalog_workloads.json)
defines standard sizes, without hidden automatic calibration. Changing sizes
requires a new report with a new manifest hash.

## Workloads

| Family | Scenarios | Standard input |
|---|---|---|
| Search | `title-search-10k`, `title-search-100k` | 10k/100k unique titles; 128 queries, 75% hit / 25% miss |
| Normalization | `normalize-title` | 10k strings: ASCII trim, an explicit ASCII/Russian case table, and comparison |
| Words | `word-frequency` | 10k strings × 10 passes, 4 words per line; owned split and frequencies for every key |
| Report | `report-builder`, `report-concat` | 10k formatted lines; builder versus a new immutable string each step |
| Maps | `map-int`, `map-string` | 4096 keys × 32 updates; identical get/put trace |
| Object map | `map-string-book` | 10k keys and Books; 4 full lookup/field-read passes |
| Set | `set-string-churn` | Live window of 4096 keys, 8 rounds of removal and insertion of fresh strings |
| Domain model | `catalog-match` | 10k Books × 32 passes, three states, payload in Loaned |
| Calls | `catalog-dotcall`, `catalog-interface` | Same 10k Books × 32; direct call and a materialized interface array |
| Identity/objects | `record-reference-copy`, `record-create` | 128 batches of 1024 retained references or fresh records |
| Array growth | `array-grow`, `array-reserved` | 100k integers × 4, without/with reserve |
| Graph representation | `bfs-int`, `bfs-record` | 4096 vertices, 16 outgoing edges, 16 traversals |
| Combined catalog | `catalog-pipeline` | 10k Books × 16: search, title frequencies, state match |
| Expected errors | `parse-result` | 10k tokens × 8, 25% invalid; parse, error propagation and match |

Integer and string maps occupy separate report rows. String-map keys are built
at runtime; the final lookup uses new strings with the same contents. Churn
inserts previously absent keys and verifies both removed-key absence and the
presence of every final key.

A Marimay Book is a record with reference identity, Go uses `*Book`, and Rust
uses `Rc<Book>`. Titles are shared by reference. This deliberately compares an
equivalent object model; Rc cost does not characterize every Rust data
representation. Go BookState is a tagged struct with a switch; Marimay and Rust
use payload enums and match. Thus `map-string-book` means `Map<string, Book>` /
`map[string]*Book` / `HashMap<Rc<str>, Rc<Book>>`.

Both BFS versions use the same topology, integer neighbor IDs, distance array
and growing queue with a head index. The record version queues Node references
and reads adjacency from each record. Degree is fixed at 16 with dense IDs;
this is not an O(V²)-edge graph, and edges are not object references. Differences
include record creation and field access, so they cannot be attributed entirely
to garbage collection.

Marimay lacks a general `lower`. `normalize-title` uses the same application
table of 59 ASCII/Russian letter pairs in every language. On this corpus,
Marimay `graphemes` yields scalar fragments, and Go/Rust construct owned scalar
strings. This is not a general Unicode-normalization, case-folding or standard
lowercase test. Words are separated by a single ASCII space; Marimay/Go/Rust
copy the tokens. Bun uses ordinary `split` and materializes scalars through
`Array.from`: JavaScript retains values independently of the source lifetime
without promising a separate physical copy. Natural-language segmentation is
outside this workload.

### TypeScript / Bun representations

All 32 scenarios retain the same inputs and checksums. `Map`/`Set` are standard
JavaScript collections; Book is a class instance with reference identity.
BookState and parse results are discriminated unions; the `Labelled` interface
is erased at runtime. An interface array is materialized and calls a method
through a helper. A separate virtual-call table is not claimed; the JIT may
specialize the call.

`number` represents these bounded integer inputs exactly: the largest
intermediate products are below 2^53. UTF-8 length uses `Buffer.byteLength`;
report checks inspect every byte from `TextEncoder`. `rune-frequency` stores
numeric Unicode code points, including non-BMP characters, preserving checksums
despite JavaScript's internal UTF-16 representation.

JavaScript has no `Array.reserve` equivalent: `array-reserved` creates
`new Array(n)` and fills indexed slots; `array-grow` uses `push`.
`report-builder` collects fragments and calls `join`, while `report-concat`
interpolates at every step. The runtime may use ropes or shared strings;
forced copying or allocation-count equalization is not added. These model
differences are part of the comparison and recorded in JSON.

## What is timed

Native: a separate Release executable, excluding compilation but including
process startup, input construction, algorithm, checksum validation, one-line
output and shutdown. VM uses `mmay run --engine vm`, including source reading,
checking and lowering. The preview does not offer a standalone public `.myb`
runner. VM therefore has its own heading and does not enter Go/Rust ratios.
VM has no `--release` flag; it uses the selected Release compiler executable.

Bun: a separate `bun --no-env-file --no-install run <entrypoint.ts>`, including
process startup, TypeScript loading/transformation, JIT, input construction,
workload and checksum. No npm dependencies are required; automatic installation
is disabled. This is a **Bun / TypeScript** column, not native AOT. Every warmup
and sample starts a fresh process; JIT state does not survive between them.
Flags, runtime version and influential JSC variables are recorded. See the
[official Bun documentation](https://bun.com/docs/runtime).

A warmup is a previous complete process, not a retained heap between iterations.
Workload/participant order rotates according to `rotating-balanced-v1`.
Statistics use `perf_counter_ns`, median, MAD, Tukey IQR, min/max, noise fraction
and a 300-second timeout. Marimay receives a 64 MiB managed heap; Go, Rust and
Bun use default memory policies. This does not equalize total RSS or every
allocator limit. JSON records relevant build/GC environment variables, runtime
profile, tool versions, commands, source/compiler/runtime/binary hashes, full
order and raw samples. Local isolation is labeled `local-unverified`.

Short cases may be dominated by startup and checksum. Noise above 30% requires
a repeat rather than a positive threshold assessment. The harness does not
choose a best repeat or discard slow successful samples. Native/Go thresholds
of 1.5× for map-int/catalog-match, 2× for map-string/words and 1.3× for algorithm
anchors are task guidelines, not release gates. No overall mean score or
general parity verdict is computed.

## Correctness and failures

The independent [`catalog_oracle.py`](catalog_oracle.py) computes expected
results from input parameters. Checks include every frequency and record, and
every UTF-8 report byte weighted by its position. Each retained record's
identity contributes to the checksum; alias/fresh scenarios differ. Every
language tests singleton input and a 17-element input with incomplete corpus
cycles. `verify.sh` runs them with differential native/VM/Go/Rust/Bun smoke.
With Bun available, `test_catalog_bun.py` compares every TypeScript scenario
against the independent oracle for singleton, 17-element partial-cycle and
smoke inputs, and checks all 11 fixed algorithms.

Wrong stdout/checksum, any stderr, nonzero exit or timeout creates a failed
cell. The first error is retained and remaining scheduled runs in that cell
become `skipped-after-failure`. Other cells continue. Partial successful samples
are retained, but a failed cell receives no median or ratio. The overall
status is `failed`; the harness returns nonzero **after saving reports**.
This exposes the engine's boundary at the original size instead of replacing
it with an easier case.

`--validate` checks report structure and internal consistency of raw samples,
order, parameters, checksums, summaries, engine labels and statuses. It does
not rerun a benchmark or attest to measurements taken on another computer.
Sources and executables must remain unchanged during measurement; the harness
checks hashes before and after.

Allocation pairs time observable object creation/retention. Heap-allocation
counts, peak RSS, GC pauses and object generations are not measured here and
cannot be inferred from traversal time; they need separate profiling. I/O,
concurrency, JSON/HTTP and scientific computing are outside this contract.
Historical rune-frequency remains a separate anchor, primarily counting an
already prepared rune array rather than decoding a large UTF-8 document on
every map update.
