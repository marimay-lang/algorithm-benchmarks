from __future__ import annotations

import hashlib
import json
import math
import pathlib
import statistics
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Optional


class ProtocolError(ValueError):
    pass


PROTOCOL_SCHEMA = "ruda.performance-protocol/1"
PROBE_RESULT_SCHEMA = "ruda.array-probes/1"
ALGORITHM_RESULT_SCHEMA = "ruda.algorithm-benchmark/2"
BUDGET_SCHEMA = "ruda.performance-budgets/1"
TIER1_TARGETS = (
    "linux-x86_64",
    "linux-arm64",
    "macos-arm64",
    "macos-x86_64",
    "windows-x86_64",
)
CORE_ALGORITHM_PARTICIPANTS = ["ruda", "go", "rust"]
LOCAL_ALGORITHM_PARTICIPANTS = ["typescript", "v", "moonbit"]


def tier1_target(system: str, machine: str) -> str:
    system_names = {
        "darwin": "macos",
        "linux": "linux",
        "windows": "windows",
    }
    machine_names = {
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "aarch64": "arm64",
        "arm64": "arm64",
    }
    normalized_system = system_names.get(system.strip().lower())
    normalized_machine = machine_names.get(machine.strip().lower())
    target = (
        f"{normalized_system}-{normalized_machine}"
        if normalized_system is not None and normalized_machine is not None
        else ""
    )
    if target not in TIER1_TARGETS:
        raise ProtocolError(
            f"unsupported Tier 1 platform metadata: {system!r}/{machine!r}"
        )
    return target


def _reject_constant(value: str) -> None:
    raise ProtocolError(f"non-finite JSON number is forbidden: {value}")


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ProtocolError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_constant,
            object_pairs_hook=_reject_duplicates,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise ProtocolError(f"{path} must contain a JSON object")
    return value


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise ProtocolError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def protocol_path(repository: pathlib.Path) -> pathlib.Path:
    return repository / "benchmarks" / "performance_protocol.json"


def load_protocol(repository: pathlib.Path) -> tuple[pathlib.Path, dict[str, Any]]:
    path = protocol_path(repository)
    protocol = load_json(path)
    if protocol.get("schema") != PROTOCOL_SCHEMA:
        raise ProtocolError(f"unsupported performance protocol in {path}")
    measurement = _mapping(protocol, "measurement")
    statistics_contract = _mapping(protocol, "statistics")
    regression = _mapping(protocol, "regression")
    resource = _mapping(protocol, "resource")
    schemas = _mapping(protocol, "result_schemas")
    _positive_int(measurement, "minimum_warmups", allow_zero=False)
    _positive_int(measurement, "minimum_samples", allow_zero=False)
    _positive_int(measurement, "timeout_seconds", allow_zero=False)
    _finite_number(statistics_contract, "maximum_baseline_noise_fraction")
    _finite_number(regression, "minimum_budget_fraction")
    _finite_number(regression, "noise_multiplier")
    _positive_int(resource, "max_heap_bytes", allow_zero=False)
    expected_schemas = {
        "probes": PROBE_RESULT_SCHEMA,
        "algorithms": ALGORITHM_RESULT_SCHEMA,
        "budgets": BUDGET_SCHEMA,
    }
    if schemas != expected_schemas:
        raise ProtocolError("performance result schema registry drifted")
    return path, protocol


def validate_run_shape(protocol: Mapping[str, Any], warmups: int, samples: int) -> None:
    measurement = _mapping(protocol, "measurement")
    minimum_warmups = _positive_int(measurement, "minimum_warmups", False)
    minimum_samples = _positive_int(measurement, "minimum_samples", False)
    if warmups < minimum_warmups:
        raise ProtocolError(
            f"insufficient warmups: {warmups}; protocol requires {minimum_warmups}"
        )
    if samples < minimum_samples:
        raise ProtocolError(
            f"insufficient samples: {samples}; protocol requires {minimum_samples}"
        )
    if measurement.get("require_odd_samples") is True and samples % 2 == 0:
        raise ProtocolError("the performance protocol requires an odd sample count")


def _median(values: Sequence[float]) -> float:
    if not values:
        raise ProtocolError("cannot summarize an empty sample set")
    return float(statistics.median(values))


def _quartiles(values: Sequence[float]) -> tuple[float, float]:
    ordered = sorted(values)
    if len(ordered) < 3:
        raise ProtocolError("at least three samples are required for quartiles")
    midpoint = len(ordered) // 2
    lower = ordered[:midpoint]
    upper = ordered[midpoint + (len(ordered) % 2) :]
    return _median(lower), _median(upper)


def summarize(samples: Sequence[float]) -> dict[str, float]:
    checked: list[float] = []
    for sample in samples:
        value = float(sample)
        if not math.isfinite(value) or value <= 0.0:
            raise ProtocolError("samples must be finite positive milliseconds")
        checked.append(value)
    median = _median(checked)
    deviations = [abs(value - median) for value in checked]
    mad = _median(deviations)
    q1, q3 = _quartiles(checked)
    iqr = q3 - q1
    noise_fraction = max(0.02, 3.0 * mad / median, iqr / median)
    return {
        "median_ms": median,
        "mad_ms": mad,
        "q1_ms": q1,
        "q3_ms": q3,
        "iqr_ms": iqr,
        "min_ms": min(checked),
        "max_ms": max(checked),
        "noise_fraction": noise_fraction,
    }


def summarize_matrix(
    raw: Mapping[str, Mapping[str, Sequence[float]]]
) -> dict[str, dict[str, dict[str, float]]]:
    return {
        workload: {
            participant: summarize(samples)
            for participant, samples in participants.items()
        }
        for workload, participants in raw.items()
    }


def _rotated(values: Sequence[str], offset: int, reverse: bool) -> list[str]:
    if not values:
        raise ProtocolError("measurement schedule cannot rotate an empty sequence")
    index = offset % len(values)
    result = list(values[index:]) + list(values[:index])
    if reverse:
        result.reverse()
    return result


def schedule(
    workloads: Sequence[str],
    participants: Sequence[str],
    warmups: int,
    samples: int,
) -> list[dict[str, Any]]:
    if len(set(workloads)) != len(workloads) or len(set(participants)) != len(participants):
        raise ProtocolError("schedule inputs must be unique")
    events: list[dict[str, Any]] = []
    rounds = [("warmup", index) for index in range(warmups)] + [
        ("sample", index) for index in range(samples)
    ]
    for global_round, (phase, phase_index) in enumerate(rounds):
        ordered_workloads = _rotated(
            workloads, global_round, reverse=global_round % 2 == 1
        )
        for workload_index, workload in enumerate(ordered_workloads):
            ordered_participants = _rotated(
                participants,
                global_round + workload_index,
                reverse=(global_round + workload_index) % 2 == 1,
            )
            for participant in ordered_participants:
                events.append(
                    {
                        "phase": phase,
                        "round": phase_index,
                        "workload": workload,
                        "participant": participant,
                    }
                )
    return events


def measure_matrix(
    commands: Mapping[str, Mapping[str, Sequence[str]]],
    expected_stdout: Mapping[str, str],
    participants: Sequence[str],
    workloads: Sequence[str],
    warmups: int,
    samples: int,
    timed_run: Callable[[Sequence[str], str], float],
) -> tuple[dict[str, dict[str, list[float]]], list[dict[str, Any]]]:
    raw = {
        workload: {participant: [] for participant in participants}
        for workload in workloads
    }
    events = schedule(workloads, participants, warmups, samples)
    for event in events:
        workload = event["workload"]
        participant = event["participant"]
        try:
            command = commands[participant][workload]
            expected = expected_stdout[workload]
        except KeyError as error:
            raise ProtocolError(f"missing measurement command: {error}") from error
        elapsed = timed_run(command, expected)
        event["elapsed_ms"] = elapsed
        if event["phase"] == "sample":
            raw[workload][participant].append(elapsed)
    return raw, events


def budget_for_summary(
    protocol: Mapping[str, Any], summary_value: Mapping[str, Any]
) -> dict[str, float]:
    statistics_contract = _mapping(protocol, "statistics")
    regression = _mapping(protocol, "regression")
    median = _finite_number(summary_value, "median_ms")
    noise = _finite_number(summary_value, "noise_fraction")
    maximum_noise = _finite_number(
        statistics_contract, "maximum_baseline_noise_fraction"
    )
    if noise > maximum_noise:
        raise ProtocolError(
            f"baseline noise {noise:.6f} exceeds protocol maximum {maximum_noise:.6f}"
        )
    fraction = max(
        _finite_number(regression, "minimum_budget_fraction"),
        _finite_number(regression, "noise_multiplier") * noise,
    )
    return {
        "baseline_median_ms": median,
        "baseline_noise_fraction": noise,
        "allowed_regression_fraction": fraction,
        "maximum_median_ms": median * (1.0 + fraction),
    }


def validate_result(
    result: Mapping[str, Any],
    protocol: Mapping[str, Any],
    protocol_sha256: str,
) -> None:
    schema = result.get("schema")
    if schema not in (PROBE_RESULT_SCHEMA, ALGORITHM_RESULT_SCHEMA):
        raise ProtocolError(f"unsupported result schema: {schema!r}")
    protocol_ref = _mapping(result, "protocol")
    if protocol_ref.get("schema") != PROTOCOL_SCHEMA:
        raise ProtocolError("result references the wrong protocol schema")
    if protocol_ref.get("sha256") != protocol_sha256:
        raise ProtocolError("result references an incompatible protocol hash")
    metadata = _mapping(result, "metadata")
    _nonempty_string(metadata, "generated_at")
    if metadata.get("clock") != "perf_counter_ns":
        raise ProtocolError("result uses the wrong measurement clock")
    if metadata.get("order") != "rotating-balanced-v1":
        raise ProtocolError("result uses the wrong order protocol")
    _nonempty_string(metadata, "command")
    warmups = _positive_int(metadata, "warmups", allow_zero=True)
    samples = _positive_int(metadata, "samples", allow_zero=False)
    validate_run_shape(protocol, warmups, samples)
    if _positive_int(metadata, "timeout_seconds", False) != _positive_int(
        _mapping(protocol, "measurement"), "timeout_seconds", False
    ):
        raise ProtocolError("result timeout is incompatible with the protocol")
    platform_data = _mapping(metadata, "platform")
    platform_identifier = _nonempty_string(platform_data, "id")
    for key in ("system", "release", "machine", "cpu"):
        _nonempty_string(platform_data, key)
    _positive_int(platform_data, "logical_cpus", allow_zero=False)
    target = tier1_target(
        _nonempty_string(platform_data, "system"),
        _nonempty_string(platform_data, "machine"),
    )
    if platform_identifier != target and not platform_identifier.startswith(
        target + "-"
    ):
        raise ProtocolError("platform id is inconsistent with system/architecture")
    isolation = _mapping(metadata, "isolation")
    if isolation.get("mode") != "dedicated-runner-contract":
        raise ProtocolError("result lacks the dedicated-runner isolation contract")
    if isolation.get("sample_selection") != "none":
        raise ProtocolError("selected/discarded samples are forbidden")
    for key in ("load_average_at_start", "load_average_at_end"):
        values = isolation.get(key)
        if not isinstance(values, list) or not all(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(float(value)) and float(value) >= 0.0
            for value in values
        ):
            raise ProtocolError(f"{key} must be a finite nonnegative list")
    _nonempty_string(isolation, "power_source")
    _nonempty_string(isolation, "affinity")
    artifacts = _mapping(metadata, "artifacts")
    compiler = _mapping(artifacts, "ruda_compiler")
    runtime = _mapping(artifacts, "runtime")
    native_c = _mapping(artifacts, "native_c")
    for artifact in (compiler, runtime):
        _sha256(artifact, "sha256")
    _nonempty_string(compiler, "path")
    for key in ("revision", "version"):
        _available_string(compiler, key)
    _sha256(runtime, "manifest_sha256")
    for key in (
        "path",
        "manifest_path",
        "runtime",
        "host",
        "processor",
        "compiler",
    ):
        _nonempty_string(runtime, key)
    if runtime.get("profile") != "release":
        raise ProtocolError("wrong runtime profile: release is required")
    if native_c.get("output_profile") != "release":
        raise ProtocolError("wrong generated-C output profile")
    for key in (
        "compiler_path",
        "compiler_version",
        "linker_path",
        "linker_version",
    ):
        _nonempty_string(native_c, key)
    for key in ("compiler_version", "linker_version"):
        _available_string(native_c, key)
    flags = native_c.get("flags")
    if not isinstance(flags, list) or not all(
        isinstance(value, str) and value for value in flags
    ):
        raise ProtocolError("generated-C flags are incomplete")
    if "-O2" not in flags and "/O2" not in flags:
        raise ProtocolError("release optimization flag is absent")
    resource = _mapping(metadata, "resource")
    if _positive_int(resource, "max_heap_bytes", False) != _positive_int(
        _mapping(protocol, "resource"), "max_heap_bytes", False
    ):
        raise ProtocolError("managed-heap budget is incompatible with the protocol")
    _nonempty_string(metadata, "corpus_revision")
    manifest_key = (
        "probe_manifest" if schema == PROBE_RESULT_SCHEMA else "equivalence_manifest"
    )
    manifest = _mapping(metadata, manifest_key)
    for key in ("path", "schema", "sha256"):
        _nonempty_string(manifest, key)
    _sha256(manifest, "sha256")
    if schema == PROBE_RESULT_SCHEMA:
        _sha256(manifest, "source_tree_sha256")
        expected_participants = {"ruda"}
        expected_toolchains = {"python", "ruda", "go", "rust"}
    else:
        languages = metadata.get("languages")
        if languages == CORE_ALGORITHM_PARTICIPANTS:
            expected_participants = set(CORE_ALGORITHM_PARTICIPANTS)
            expected_toolchains = {"python", *CORE_ALGORITHM_PARTICIPANTS}
        else:
            if not isinstance(languages, list):
                raise ProtocolError("algorithm result lacks the complete language matrix")
            extras = languages[len(CORE_ALGORITHM_PARTICIPANTS) :]
            expected_extras = [
                language
                for language in LOCAL_ALGORITHM_PARTICIPANTS
                if language in extras
            ]
            if (
                languages[: len(CORE_ALGORITHM_PARTICIPANTS)]
                != CORE_ALGORITHM_PARTICIPANTS
                or not extras
                or extras != expected_extras
                or len(set(languages)) != len(languages)
            ):
                raise ProtocolError("algorithm result has an invalid local language matrix")
            if metadata.get("comparison_scope") != "local-only":
                raise ProtocolError("extended algorithm result must be marked local-only")
            local_manifest = _mapping(metadata, "local_participants_manifest")
            for key in ("path", "schema", "sha256"):
                _nonempty_string(local_manifest, key)
            _sha256(local_manifest, "sha256")
            if local_manifest.get("schema") != "ruda.local-benchmark-participants/1":
                raise ProtocolError("extended algorithm result has the wrong local manifest")
            expected_participants = set(languages)
            expected_toolchains = {"python", *CORE_ALGORITHM_PARTICIPANTS, *extras}
    toolchains = _mapping(metadata, "toolchains")
    if set(toolchains) != expected_toolchains:
        raise ProtocolError("toolchain metadata is incomplete")
    for key in toolchains:
        _available_string(toolchains, key)
    workloads = _mapping(result, "workloads")
    if not workloads:
        raise ProtocolError("result has no workloads")
    participant_names: Optional[set[str]] = None
    for workload, observation_value in workloads.items():
        if not isinstance(workload, str) or not workload:
            raise ProtocolError("workload ids must be non-empty strings")
        observation = _mapping_value(observation_value, f"workload {workload}")
        _nonempty_string(observation, "description")
        checksum = observation.get("expected_checksum")
        if isinstance(checksum, bool) or not isinstance(checksum, int):
            raise ProtocolError(f"{workload} checksum metadata is invalid")
        expected = _nonempty_string(observation, "expected_stdout")
        if expected != f"{workload} {checksum}\n":
            raise ProtocolError(f"{workload} checksum/stdout contract drifted")
        raw = _mapping(observation, "raw_ms")
        summaries = _mapping(observation, "summary")
        commands = _mapping(observation, "commands")
        current_names = set(raw)
        if participant_names is None:
            participant_names = current_names
        elif current_names != participant_names:
            raise ProtocolError("workloads have inconsistent participant sets")
        if set(summaries) != current_names:
            raise ProtocolError(f"{workload} summary/raw participant mismatch")
        if set(commands) != current_names:
            raise ProtocolError(f"{workload} command/raw participant mismatch")
        if current_names != expected_participants:
            raise ProtocolError(f"{workload} participant matrix is incomplete")
        for participant, command in commands.items():
            if not isinstance(command, list) or not command or not all(
                isinstance(argument, str) and argument for argument in command
            ):
                raise ProtocolError(f"{workload}/{participant} command is incomplete")
        for participant, sample_value in raw.items():
            if not isinstance(sample_value, list) or len(sample_value) != samples:
                raise ProtocolError(
                    f"{workload}/{participant} has insufficient samples"
                )
            calculated = summarize(sample_value)
            recorded = _mapping_value(
                summaries[participant], f"{workload}/{participant} summary"
            )
            if set(recorded) != set(calculated):
                raise ProtocolError(f"{workload}/{participant} summary is incomplete")
            for key, value in calculated.items():
                actual = _finite_number(recorded, key)
                if not math.isclose(actual, value, rel_tol=1e-12, abs_tol=1e-9):
                    raise ProtocolError(
                        f"{workload}/{participant} summary drift for {key}"
                    )
    order = result.get("order")
    first_observation = next(iter(workloads.values()))
    first_raw = _mapping(_mapping_value(first_observation, "first workload"), "raw_ms")
    participants = list(first_raw)
    expected_order = schedule(list(workloads), participants, warmups, samples)
    if not isinstance(order, list) or len(order) != len(expected_order):
        raise ProtocolError("measurement order trace is incomplete")
    measured_counts: dict[tuple[str, str], int] = {}
    for index, event in enumerate(order):
        event_map = _mapping_value(event, "measurement order event")
        expected_event = expected_order[index]
        for key in ("phase", "round", "workload", "participant"):
            if event_map.get(key) != expected_event[key]:
                raise ProtocolError("measurement order trace violates rotation protocol")
        phase = event_map.get("phase")
        if phase not in ("warmup", "sample"):
            raise ProtocolError("measurement order has an invalid phase")
        elapsed = _finite_number(event_map, "elapsed_ms")
        if elapsed <= 0:
            raise ProtocolError("measurement order contains a non-positive sample")
        key = (str(event_map.get("workload")), str(event_map.get("participant")))
        if phase == "sample":
            measured_counts[key] = measured_counts.get(key, 0) + 1
    if any(count != samples for count in measured_counts.values()) or len(
        measured_counts
    ) != len(workloads) * len(participants):
        raise ProtocolError("measurement order does not cover every raw sample")


def validate_compatible_results(
    probes: Mapping[str, Any], algorithms: Mapping[str, Any]
) -> None:
    if probes.get("schema") != PROBE_RESULT_SCHEMA:
        raise ProtocolError("first result is not an array-probe result")
    if algorithms.get("schema") != ALGORITHM_RESULT_SCHEMA:
        raise ProtocolError("second result is not an algorithm result")
    left = _mapping(probes, "metadata")
    right = _mapping(algorithms, "metadata")
    if right.get("comparison_scope") == "local-only":
        raise ProtocolError("local-only algorithm results cannot be Tier 1 baselines")
    checks = [
        ("platform", _mapping(left, "platform").get("id"), _mapping(right, "platform").get("id")),
        ("Ruda compiler", _mapping(_mapping(left, "artifacts"), "ruda_compiler").get("sha256"), _mapping(_mapping(right, "artifacts"), "ruda_compiler").get("sha256")),
        ("runtime", _mapping(_mapping(left, "artifacts"), "runtime").get("sha256"), _mapping(_mapping(right, "artifacts"), "runtime").get("sha256")),
        ("resource budget", _mapping(left, "resource").get("max_heap_bytes"), _mapping(right, "resource").get("max_heap_bytes")),
        ("samples", left.get("samples"), right.get("samples")),
        ("warmups", left.get("warmups"), right.get("warmups")),
    ]
    for label, first, second in checks:
        if first != second:
            raise ProtocolError(f"incompatible {label}: {first!r} != {second!r}")
    if probes.get("protocol") != algorithms.get("protocol"):
        raise ProtocolError("results use different measurement protocols")


def validate_budget(
    budget: Mapping[str, Any],
    probes: Mapping[str, Any],
    algorithms: Mapping[str, Any],
    protocol_sha256: str,
) -> list[str]:
    if _mapping(algorithms, "metadata").get("comparison_scope") == "local-only":
        raise ProtocolError("local-only algorithm results cannot use Tier 1 budgets")
    if budget.get("schema") != BUDGET_SCHEMA:
        raise ProtocolError("unsupported performance budget schema")
    if budget.get("protocol_sha256") != protocol_sha256:
        raise ProtocolError("budget uses an incompatible protocol")
    review = _mapping(budget, "review")
    if review.get("status") != "reviewed":
        raise ProtocolError("performance budget has not been reviewed")
    _nonempty_string(review, "reviewed_at")
    _nonempty_string(review, "rationale")
    platform_id = _nonempty_string(budget, "platform_id")
    actual_platform = _mapping(_mapping(probes, "metadata"), "platform").get("id")
    if platform_id != actual_platform:
        raise ProtocolError("budget platform is incompatible with results")
    baseline = _mapping(budget, "baseline")
    for key in ("probe_result", "algorithm_result"):
        _nonempty_string(baseline, key)
    for key in ("probe_result_sha256", "algorithm_result_sha256"):
        _sha256(baseline, key)
    probe_metadata = _mapping(probes, "metadata")
    algorithm_metadata = _mapping(algorithms, "metadata")
    probe_compiler = _mapping(_mapping(probe_metadata, "artifacts"), "ruda_compiler")
    algorithm_compiler = _mapping(
        _mapping(algorithm_metadata, "artifacts"), "ruda_compiler"
    )
    bindings = (
        (
            "Ruda revision",
            _nonempty_string(baseline, "ruda_revision"),
            _nonempty_string(probe_compiler, "revision"),
            _nonempty_string(algorithm_compiler, "revision"),
        ),
        (
            "corpus revision",
            _nonempty_string(baseline, "corpus_revision"),
            _nonempty_string(probe_metadata, "corpus_revision"),
            _nonempty_string(algorithm_metadata, "corpus_revision"),
        ),
        (
            "probe manifest",
            _sha256(baseline, "probe_manifest_sha256"),
            _sha256(_mapping(probe_metadata, "probe_manifest"), "sha256"),
            _sha256(_mapping(probe_metadata, "probe_manifest"), "sha256"),
        ),
        (
            "equivalence manifest",
            _sha256(baseline, "equivalence_manifest_sha256"),
            _sha256(
                _mapping(algorithm_metadata, "equivalence_manifest"), "sha256"
            ),
            _sha256(
                _mapping(algorithm_metadata, "equivalence_manifest"), "sha256"
            ),
        ),
    )
    for label, recorded, first, second in bindings:
        if recorded != first or recorded != second:
            raise ProtocolError(f"budget baseline {label} is incompatible with results")
    suites = _mapping(budget, "suites")
    failures: list[str] = []
    for suite_name, result in (("probes", probes), ("algorithms", algorithms)):
        suite_budget = _mapping(suites, suite_name)
        result_workloads = _mapping(result, "workloads")
        if set(suite_budget) != set(result_workloads):
            raise ProtocolError(f"{suite_name} budget workload set is incompatible")
        for workload, limit_value in suite_budget.items():
            limit = _mapping_value(limit_value, f"{suite_name}/{workload} budget")
            maximum = _finite_number(limit, "maximum_median_ms")
            if maximum <= 0:
                raise ProtocolError("budget maximum must be positive")
            for key in (
                "baseline_median_ms",
                "baseline_noise_fraction",
                "allowed_regression_fraction",
            ):
                if _finite_number(limit, key) < 0:
                    raise ProtocolError(f"budget {key} must be non-negative")
            summary_value = _mapping(
                _mapping_value(result_workloads[workload], workload), "summary"
            )
            ruda_summary = _mapping_value(summary_value.get("ruda"), workload)
            actual = _finite_number(ruda_summary, "median_ms")
            if actual > maximum:
                failures.append(
                    f"{suite_name}/{workload}: {actual:.6f} ms > {maximum:.6f} ms"
                )
    return failures


def validate_budget_files(
    budget: Mapping[str, Any],
    repository: pathlib.Path,
    probes_path: pathlib.Path,
    algorithms_path: pathlib.Path,
) -> None:
    baseline = _mapping(budget, "baseline")
    repository = repository.resolve()
    paths = (
        (
            "probe",
            probes_path.resolve(),
            _nonempty_string(baseline, "probe_result"),
            _sha256(baseline, "probe_result_sha256"),
        ),
        (
            "algorithm",
            algorithms_path.resolve(),
            _nonempty_string(baseline, "algorithm_result"),
            _sha256(baseline, "algorithm_result_sha256"),
        ),
    )
    for label, path, recorded_path, recorded_hash in paths:
        try:
            relative = path.relative_to(repository).as_posix()
        except ValueError as error:
            raise ProtocolError(
                f"{label} result is outside the benchmark repository"
            ) from error
        if recorded_path != relative:
            raise ProtocolError(f"budget baseline {label} result path drifted")
        if recorded_hash != sha256_file(path):
            raise ProtocolError(f"budget baseline {label} result checksum drifted")


def _mapping(container: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    return _mapping_value(container.get(key), key)


def _mapping_value(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ProtocolError(f"{label} must be an object")
    return value


def _positive_int(container: Mapping[str, Any], key: str, allow_zero: bool) -> int:
    value = container.get(key)
    minimum = 0 if allow_zero else 1
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ProtocolError(f"{key} must be an integer >= {minimum}")
    return value


def _finite_number(container: Mapping[str, Any], key: str) -> float:
    value = container.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ProtocolError(f"{key} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ProtocolError(f"{key} must be finite")
    return result


def _nonempty_string(container: Mapping[str, Any], key: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value:
        raise ProtocolError(f"{key} must be a non-empty string")
    return value


def _available_string(container: Mapping[str, Any], key: str) -> str:
    value = _nonempty_string(container, key)
    if value.strip().lower() in {"unknown", "unavailable", "pending"}:
        raise ProtocolError(f"{key} metadata is unavailable")
    return value


def _sha256(container: Mapping[str, Any], key: str) -> str:
    value = _nonempty_string(container, key)
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ProtocolError(f"{key} must be a lowercase SHA-256")
    return value
