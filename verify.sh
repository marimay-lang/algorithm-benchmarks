#!/usr/bin/env bash

set -euo pipefail

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mmay_binary=${MMAY:-"$repository_root/../Ma/build/rebrand-debug/mmay"}

if [[ ! -x "$mmay_binary" ]]; then
  echo "Marimay executable not found: $mmay_binary" >&2
  echo "Build Marimay or set MMAY=/absolute/path/to/mmay" >&2
  exit 2
fi

verify_tmp=$(mktemp -d)
cleanup() {
  if [[ -n "${verify_tmp:-}" && -d "$verify_tmp" ]]; then
    rm -rf -- "$verify_tmp"
  fi
}
trap cleanup EXIT

expect_stdout() {
  local label=$1
  local expected=$2
  shift 2
  local actual_path="$verify_tmp/$label.actual"
  local expected_path="$verify_tmp/$label.expected"
  printf '%s' "$expected" >"$expected_path"
  "$@" >"$actual_path"
  if ! cmp -s "$expected_path" "$actual_path"; then
    echo "unexpected stdout for $label" >&2
    diff -u "$expected_path" "$actual_path" >&2 || true
    exit 1
  fi
}

python3 "$repository_root/benchmarks/validate_equivalence.py"
python3 -m unittest discover -s "$repository_root/benchmarks" -p 'test_*.py'
python3 "$repository_root/benchmarks/validate_tier1_baselines.py" \
  --gate checkpoint-21

echo "== Marimay =="
"$mmay_binary" fmt "$repository_root/marimay" --check
"$mmay_binary" check "$repository_root/marimay"
"$mmay_binary" check "$repository_root/marimay/benchmarks/core"
expect_stdout marimay-vm $'Marimay algorithms: ok\n' \
  "$mmay_binary" run "$repository_root/marimay"
expect_stdout marimay-test-both \
  $'test study/algorithms.sortingAlgorithms ... ok\n'\
$'test study/algorithms.dataStructures ... ok\n'\
$'test study/algorithms.graphAlgorithms ... ok\n'\
$'test study/algorithms.invalidGraphInputsAreRejected ... ok\n'\
$'test result: ok. 4 passed; 0 failed\n' \
  "$mmay_binary" test "$repository_root/marimay" --engine both
"$mmay_binary" build "$repository_root/marimay" --output "$verify_tmp/marimay-algorithms-debug"
expect_stdout marimay-native-debug $'Marimay algorithms: ok\n' \
  "$verify_tmp/marimay-algorithms-debug"
"$mmay_binary" build "$repository_root/marimay" --release --output "$verify_tmp/marimay-algorithms-release"
expect_stdout marimay-native-release $'Marimay algorithms: ok\n' \
  "$verify_tmp/marimay-algorithms-release"

echo "== Go =="
(
  cd "$repository_root/go"
  test -z "$(gofmt -l .)"
  go vet ./...
  go test ./...
  expect_stdout go-correctness $'Go algorithms: ok\n' go run .
)

echo "== Rust =="
(
  cd "$repository_root/rust"
  cargo fmt --all -- --check
  cargo clippy --all-targets -- -D warnings
  cargo test --all-targets
  expect_stdout rust-correctness $'Rust algorithms: ok\n' \
    cargo run --quiet --bin marimay-algorithms
)

echo "== Benchmark harness =="
python3 -m py_compile \
  "$repository_root/benchmarks/derive_budget.py" \
  "$repository_root/benchmarks/equivalence.py" \
  "$repository_root/benchmarks/local_languages.py" \
  "$repository_root/benchmarks/local_participants.py" \
  "$repository_root/benchmarks/perf_environment.py" \
  "$repository_root/benchmarks/perf_protocol.py" \
  "$repository_root/benchmarks/probe_manifest.py" \
  "$repository_root/benchmarks/probes.py" \
  "$repository_root/benchmarks/run.py" \
  "$repository_root/benchmarks/test_equivalence.py" \
  "$repository_root/benchmarks/test_local_participants.py" \
  "$repository_root/benchmarks/test_perf_environment.py" \
  "$repository_root/benchmarks/test_perf_protocol.py" \
  "$repository_root/benchmarks/test_probe_manifest.py" \
  "$repository_root/benchmarks/test_probes.py" \
  "$repository_root/benchmarks/test_tier1_baselines.py" \
  "$repository_root/benchmarks/tier1_baselines.py" \
  "$repository_root/benchmarks/validate_equivalence.py" \
  "$repository_root/benchmarks/validate_results.py" \
  "$repository_root/benchmarks/validate_tier1_baselines.py"

echo "All supported checks passed."
