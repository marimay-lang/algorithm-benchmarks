# Benchmark methodology

For application comparisons of catalogs, text, collections, records, interfaces
and errors, [`make benchmark-comprehensive`](CATALOG.md) adds 21 scenarios to
11 algorithm anchors across Marimay native/VM, Go, Rust and Bun. The harness
does not compute a language-wide Go-parity verdict.

By default, `run.py` compares eight identical deterministic workloads in
Marimay, Go and Rust. `--expanded` adds three local-only workloads for `Map`,
`Set` and Unicode `rune`, defined in
[`expanded_workloads.json`](expanded_workloads.json). `probes.py` separately
measures nine focused Marimay workloads that isolate scalar get/set, provable
and dynamic bounds, growth/reserve, dense scalar storage, nested traversal
and checked integer loops. Both harnesses use `mmay build --release` with a
fixed managed-heap budget, then measure native executables directly.
Compilation and `mmay run`/VM are outside these results.

[`equivalence.json`](equivalence.json) is the machine-readable workload
contract: LCG, checksums, sizes, operations, representations, selected checks
and reusable entrypoint markers. [`validate_equivalence.py`](validate_equivalence.py)
checks the contract and sources before any build; `run.py` does not maintain
a second constant list. The compatible toolchain is pinned separately in
[`marimay-toolchain.json`](marimay-toolchain.json). Every harness checks
machine-readable `mmay version --json` before creating benchmark artifacts.

Run the expanded local matrix with:

```sh
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/run.py --expanded --samples 11 --warmups 3 \
  --output benchmarks/results/expanded-algorithms-local.md
```

It includes all eleven algorithms in Marimay, Go and Rust with the same
measurement protocol and checksum gate, labeled `local-only`. New workloads
do not rewrite the historical eight-workload manifest or automatically enter
the checkpoint-21 budget.

[`performance_protocol.json`](performance_protocol.json) defines the
checkpoint-21 contract: Release profile, 3 warmups and at least 11 samples
(with an odd sample count), 300-second per-process timeout, balanced rotating
workload/language order, `perf_counter_ns`, median, MAD, Tukey IQR, a noise
envelope, a 64 MiB heap budget, and exactly one full retry after cooldown.
[`probes.json`](probes.json) owns probe IDs, cost categories, entrypoints
and checksums.

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

After review, each platform budget is added to
[`tier1-baselines.json`](tier1-baselines.json). `make benchmark-validate`
implements the checkpoint-21 gate for the dedicated Linux x86_64 runner,
rechecking raw schemas/current manifests and binding the reviewed budget to
exact result paths/SHA-256. `make benchmark-validate-public-alpha` is a
separate deferred gate requiring a compatible baseline for Linux x86_64,
Linux arm64, macOS arm64, macOS x86_64 and Windows x86_64. Checkpoint-21
completion therefore does not establish full public-alpha Tier 1 readiness.
`make benchmark-validate-platform` separately validates the Linux baseline.

The default compiler is `../marimay/build/release/mmay`. Since checkpoint 13,
the requested output profile selects a matching Release runtime independently
of the compiler executable's build profile. The harness checks the runtime
manifest rather than inferring its profile from the compiler path.

`--skip-build` is for an immediate local repeat of already verified artifacts.
A published-baseline command always builds executables first. Tier 1 algorithm
reports contain the complete `marimay,go,rust` set in protocol order. Focused
checkpoint reports may select an ordered subset with `--languages`, carrying
`measurement_scope=focused`; they are candidates rather than reviewed Tier 1
baselines.

Since checkpoint 24, focused performance gates can build just the relevant
probe group without changing the measurement protocol:

```sh
./benchmarks/probes.py --probe capacity --output benchmarks/results/cp25-capacity-PLATFORM.json
./benchmarks/probes.py --probe nested-traversal --output benchmarks/results/cp26-nested-PLATFORM.json
./benchmarks/probes.py --probe checked-integer --output benchmarks/results/cp27-integer-PLATFORM.json
./benchmarks/validate_results.py benchmarks/results/cp25-capacity-PLATFORM.json
```

`capacity` selects `growth` and `reserved-growth`; `nested-traversal` and
`checked-integer` select the corresponding nested probe and `checked-loop`.
The validator accepts full or focused candidates and compares present
workloads to reviewed platform ceilings. Checkpoint-21 baselines themselves
retain exact path/SHA-256 binding. `--baseline` accepts a historical algorithm
report with the same platform/workload set as comparison context, without
replacing the reviewed budget.

## Local-only language feature probes

New language features are measured separately from the historical array/native
manifest, preserving its source hashes and reviewed budgets. Feature probes
use the same Release profile, 64 MiB managed heap, 3 warmups + 11 samples,
raw timings and noise statistics, with a separate schema and always
`comparison_scope=local-only`:

```sh
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/feature_probes.py --feature dynamic-text \
  --output benchmarks/results/cp30-dynamic-text-local.json
```

`dynamic-text` measures interpolation, int/bool formatting, string construction
and `parseInt` in one deterministic loop. The first report is a candidate;
a published threshold requires a separate decision and repeatable baseline
under D056.

The historical `cp21-baseline.yml` workflow retains its original filename.
It was configured to run the CP30 regression matrix on Linux x86_64 for pushes
to `main`: 9 probes and 8 algorithms against reviewed checkpoint-21 ceilings,
a separate `cp30-dynamic-text-linux-x86_64.json` without an automatic threshold,
and raw evidence in `evidence/cp30-linux-x86_64-<revision>`. Historical Gitea
workflow files do not by themselves enable GitHub Actions.

## Optional local language participants

TypeScript/Bun, V and MoonBit are enabled only by explicitly extending the
canonical matrix:

```sh
MMAY=/absolute/path/to/release/mmay \
  ./benchmarks/run.py \
  --languages marimay,go,rust,typescript,v,moonbit \
  --samples 11 --warmups 3 \
  --output benchmarks/results/local-six-languages.md
```

Select local tools with `BUN`, `V` and `MOON`. Bun builds TypeScript into a
standalone executable; V builds a production native executable; MoonBit builds
a Release native executable. [`local_participants.json`](local_participants.json)
binds their sources, workload IDs and checksums to canonical
[`equivalence.json`](equivalence.json), preserving historical Tier 1 hashes.

Expanded results always carry `comparison_scope: local-only`; they cannot be
used by `validate_results.py`, reviewed budgets or the Tier 1 registry.
`verify.sh` checks manifests, source contracts and negative protocol tests.
Optional algorithm participants are separate from the canonical
`marimay,go,rust` matrix; the catalog verification path additionally requires
Bun, as described in [`CATALOG.md`](CATALOG.md).

## What is measured

- Each language's Release/optimized native executable.
- The same LCG: `state = (state * 25173 + 13849) % 65536`.
- Identical sizes, repetitions and reusable algorithms.
- For expanded workloads, matching hash-map/hash-set representations and the
  same Unicode-scalar sequence.
- Wall-clock time from process startup through exit.
- Median of at least 11 executions after at least 3 warmups.
- MAD, IQR, min/max, noise fraction, every raw sample and actual order.

Each process prints exactly `<benchmark> <checksum>\n`, without stderr.
The harness rejects different checksums, output bytes, exit status or timeouts.
Workload/language order rotates between rounds to avoid a systematic advantage
for a consistently first or last participant. Timing includes process startup,
input initialization and one stdout line; input is created within the process.

Correctness suites separately reject out-of-range graph starts/endpoints and
negative Dijkstra weights. Invalid-input probes are outside timing. Rust graph
indices use `usize`, excluding signed negative indices by representation,
as recorded in the manifest.

## Isolation, metadata and budgets

Before a baseline, the operator reserves a runner without parallel repository
jobs, records the power policy, prevents automatic sleep for the interval and
does not select best samples. JSON retains platform/CPU/load/power metadata,
full toolchain versions, commands, compiler/runtime paths and SHA-256,
runtime manifest/profile, generated-C compiler/linker versions and flags,
corpus/manifest revisions and resource budgets.

The validator rejects a Debug runtime, incomplete metadata, NaN/Infinity,
insufficient samples, incompatible baselines and checksum/source-manifest drift.
A threshold is per Marimay workload and platform rather than a cross-language
ratio:
`baseline median × (1 + max(10%, noise envelope))`, where the envelope is the
maximum of 2%, `3 × MAD / median` and `IQR / median`.

An excess requires one full 11/3 repeat after cooldown. A Release regression
is confirmed only if both independent medians exceed the same reviewed budget.
Automatic retry does not turn a flaky failure into a pass; both raw reports
are retained.

## Results

The checkpoint-21 Linux x86_64 baseline is recorded in
[`results/cp21-algorithms-linux-x86_64.md`](results/cp21-algorithms-linux-x86_64.md),
[`results/cp21-algorithms-linux-x86_64.json`](results/cp21-algorithms-linux-x86_64.json)
and [`results/cp21-probes-linux-x86_64.json`](results/cp21-probes-linux-x86_64.json).
Reviewed thresholds are in
[`budgets/cp21-linux-x86_64.json`](budgets/cp21-linux-x86_64.json).

The earlier additional macOS arm64/Apple M2 baseline is recorded in
[`results/cp21-algorithms-macos-arm64-apple-m2.md`](results/cp21-algorithms-macos-arm64-apple-m2.md),
[`results/cp21-algorithms-macos-arm64-apple-m2.json`](results/cp21-algorithms-macos-arm64-apple-m2.json)
and [`results/cp21-probes-macos-arm64-apple-m2.json`](results/cp21-probes-macos-arm64-apple-m2.json).
Reviewed thresholds are in
[`budgets/cp21-macos-arm64-apple-m2.json`](budgets/cp21-macos-arm64-apple-m2.json).
This remains retained public-alpha evidence without extending the checkpoint-21
completion contract. Until measurement and review, the public-alpha gate lists
missing Linux arm64, macOS x86_64 and Windows x86_64 baselines.

Legacy `results/latest.*`, Debug-runtime baselines and checkpoint-20 smoke are
historical local evidence; they do not satisfy the checkpoint-21 schema.
Named raw reports and a compatible reviewed platform budget form the regression
gate. Cross-language rankings and universal speed claims remain outside scope.

Historical reports may contain privacy-transformed paths. See [publication provenance](results/PUBLICATION-PROVENANCE.md) for original and public receipt hashes and the unchanged measurement/source identity contract.
