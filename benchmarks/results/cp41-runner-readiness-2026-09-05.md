# CP41 runner readiness — 2026-09-05

Status: diagnostic infrastructure evidence, not a timing baseline, performance
result, or CP41 completion claim. No benchmark samples are selected or discarded
by this report.

The exact compiler pair remains:

- before: `5963290287a6d5e41cf144065ba424d5902d569f`;
- after: `01aec63307be70136b5375fd32a0091de11fb0f1`, the merged compiler main
  including CP39, CP41, CLI application fixes, and Map/Set optimizations.

The corpus implementations, work counts, checksums, D056 protocol, acceptance
thresholds, and `linux-l1d-loads-v1` counter profile were not changed.

## Executed checks

[Run 177](http://gitea.example.invalid:3000/Marimay/algorithm-benchmarks/actions/runs/177/jobs/1438)
at corpus `eb2741b1f193e568fedf155e393a9dc4f32c7186` passed container setup and
both exact compiler checkouts. The toolchain check then failed because
`find -type f` excluded the Ubuntu-packaged `perf` symlink. Commit
`d255871efc241096e47ee5f0cb3e10beba8d36d9` resolves that link consistently with
the existing counter preflight. A local symlink fixture reproduced the old
empty match and verified the corrected executable lookup; all 76 Python
harness tests and the pinned-image reference check passed.

[Run 178](http://gitea.example.invalid:3000/Marimay/algorithm-benchmarks/actions/runs/178/jobs/1439)
at that corrected corpus revision passed toolchain verification, the positive
hardware-counter preflight, and both exact Release compiler builds. It was
explicitly canceled before the wall-clock collection step because host
isolation was not suitable for a reviewed measurement.

The runner identity step recorded Linux x86_64, four logical CPUs, KVM/QEMU,
Clang 18.1.3, Go 1.26.6, Rust 1.96.0, and load averages
`70.29 65.08 38.44`. The repository-scoped `gitea-runner-cp41-perf` runner was
online and initially idle, but that scheduling label did not establish CPU/VM
isolation. Ordinary compiler CI was concurrently active. This report does not
infer the exact infrastructure topology from load averages alone.

## Required next action

Confirm whether the performance runner shares its VM/physical resources with
ordinary CI. Allow those jobs to finish, establish the D056 host-isolation and
power/sleep conditions, and cool down before one complete new before/after
run. Do not cancel unrelated jobs or silently provision/change runner
privileges. Preserve every valid sample from that future run and apply the
unchanged acceptance contract. Counter availability is now evidenced; timing,
cross-target code-generation reductions, and complete CP41 acceptance are not.
