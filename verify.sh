#!/usr/bin/env bash

set -euo pipefail

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ruda_binary=${RUDA:-"$repository_root/../Ma/build/debug/ruda"}

if [[ ! -x "$ruda_binary" ]]; then
  echo "Ruda executable not found: $ruda_binary" >&2
  echo "Build Ruda or set RUDA=/absolute/path/to/ruda" >&2
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

echo "== Ruda =="
"$ruda_binary" fmt "$repository_root/ruda" --check
"$ruda_binary" check "$repository_root/ruda"
"$ruda_binary" check "$repository_root/ruda/benchmarks/core"
expect_stdout ruda-vm $'Ruda algorithms: ok\n' \
  "$ruda_binary" run "$repository_root/ruda"
expect_stdout ruda-test-both \
  $'test study/algorithms.sortingAlgorithms ... ok\n'\
$'test study/algorithms.dataStructures ... ok\n'\
$'test study/algorithms.graphAlgorithms ... ok\n'\
$'test study/algorithms.invalidGraphInputsAreRejected ... ok\n'\
$'test result: ok. 4 passed; 0 failed\n' \
  "$ruda_binary" test "$repository_root/ruda" --engine both
"$ruda_binary" build "$repository_root/ruda" --output "$verify_tmp/ruda-algorithms-debug"
expect_stdout ruda-native-debug $'Ruda algorithms: ok\n' \
  "$verify_tmp/ruda-algorithms-debug"
"$ruda_binary" build "$repository_root/ruda" --release --output "$verify_tmp/ruda-algorithms-release"
expect_stdout ruda-native-release $'Ruda algorithms: ok\n' \
  "$verify_tmp/ruda-algorithms-release"

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
    cargo run --quiet --bin ruda-algorithms
)

echo "== Benchmark harness =="
python3 -m py_compile \
  "$repository_root/benchmarks/derive_budget.py" \
  "$repository_root/benchmarks/equivalence.py" \
  "$repository_root/benchmarks/perf_environment.py" \
  "$repository_root/benchmarks/perf_protocol.py" \
  "$repository_root/benchmarks/probe_manifest.py" \
  "$repository_root/benchmarks/probes.py" \
  "$repository_root/benchmarks/run.py" \
  "$repository_root/benchmarks/test_equivalence.py" \
  "$repository_root/benchmarks/test_perf_environment.py" \
  "$repository_root/benchmarks/test_perf_protocol.py" \
  "$repository_root/benchmarks/test_probe_manifest.py" \
  "$repository_root/benchmarks/test_tier1_baselines.py" \
  "$repository_root/benchmarks/tier1_baselines.py" \
  "$repository_root/benchmarks/validate_equivalence.py" \
  "$repository_root/benchmarks/validate_results.py" \
  "$repository_root/benchmarks/validate_tier1_baselines.py"

echo "All supported checks passed."
