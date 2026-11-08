"""Human-readable interpretation with engine and coverage boundaries."""

from __future__ import annotations

LABELS = {
    "marimay-native": "Marimay native",
    "go": "Go native",
    "rust": "Rust native",
    "marimay-vm": "Marimay VM (source run)",
    "bun": "Bun / TypeScript",
}


def console_report(result):
    meta = result["metadata"]
    participants = meta["participants"]
    rows = [["Workload", *[LABELS[p] for p in participants]]]
    failures = []
    for identifier, row in result["workloads"].items():
        rows.append(
            [identifier]
            + [
                f"{row['summary'][p]['median_ms']:.2f}"
                if row["summary"][p] is not None
                else "FAILED"
                for p in participants
            ]
        )
        for participant in participants:
            outcome = row["outcomes"][participant]
            if outcome["status"] == "failed":
                failures.append(
                    f"{identifier} / {LABELS[participant]}: {outcome['error']}"
                )
    widths = [max(len(cell) for cell in column) for column in zip(*rows)]
    lines = [
        f"\nMedian time, ms ({meta['warmups']} warmups, {meta['samples']} samples):"
    ]
    for row in rows:
        lines.append("  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip())
    if "marimay-vm" in participants:
        lines.append("\nVM includes source loading, checking and lowering.")
    if "bun" in participants:
        lines.append("Bun includes process startup, TypeScript loading and JIT; each observation uses a fresh process.")
    lines.append(f"Status: {result['status']}")
    lines.extend(failures)
    return "\n".join(lines)


def markdown_report(result):
    meta = result["metadata"]
    participants = meta["participants"]
    comparison = (
        "marimay-native" in participants
        and meta["profile"] == "standard"
        and not meta["verify_only"]
    )
    lines = [
        "# Catalogue and language benchmark",
        "",
        f"Generated: {meta['generated_at']}; profile: **{meta['profile']}**; scope: **local-only**; status: **{result['status']}**.",
        "",
        f"Host: {meta['platform']['system']} {meta['platform']['machine']}; {meta['platform']['cpu']}.",
        "",
        f"Samples: **{meta['samples']}** after **{meta['warmups']}** process warmups; timeout: {meta['timeout_seconds']} s; Marimay managed heap: {meta['resource']['max_heap_bytes']} bytes.",
        "",
        "Native columns measure release executables directly, including input generation, checksum, process startup and teardown. Compilation is excluded. VM uses `mmay run --engine vm`: source loading, checking and lowering are included. VM timings are not used for Go/Rust ratios.",
        "",
        "Local host isolation is not independently verified. Raw samples, order, commands, sources and executable SHA-256, runtime and toolchain metadata are in the companion JSON.",
        "",
    ]
    if not comparison:
        lines += [
            "**Diagnostic/correctness run: no performance or parity conclusion.**",
            "",
        ]
    if "bun" in participants:
        lines += [
            "Bun runs TypeScript source with JavaScriptCore JIT and default GC. Each observation starts a fresh process; TypeScript loading/transpilation and JIT work are included. Process warmups do not retain a warmed JIT. Bun is not a native AOT column. See the representation differences in the catalogue methodology.",
            "",
        ]
    headers = ["Workload", "Size × rounds", *[LABELS[p] + " ms" for p in participants]]
    if comparison:
        headers += ["native / Go", "native / Rust", "Go target", "Assessment"]
    lines += ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for identifier, row in result["workloads"].items():
        stats = row["summary"]
        params = row.get("parameters")
        cells = [
            identifier,
            f"{params['size']:,} × {params['rounds']}" if params else "fixed anchor",
        ]
        cells += [
            f"{stats[p]['median_ms']:.2f}" if stats[p] is not None else "**FAILED**"
            for p in participants
        ]
        if comparison and any(
            stats[p] is None for p in ("marimay-native", "go", "rust")
        ):
            cells += ["—", "—", "—", "incomplete"]
        elif comparison:
            go_ratio = stats["marimay-native"]["median_ms"] / stats["go"]["median_ms"]
            rust_ratio = (
                stats["marimay-native"]["median_ms"] / stats["rust"]["median_ms"]
            )
            target = row.get("go_ratio_target")
            cells += [
                f"{go_ratio:.2f}×",
                f"{rust_ratio:.2f}×",
                f"≤ {target:.1f}×" if target else "—",
            ]
            noisy = any(
                stats[p]["noise_fraction"] > 0.30
                for p in ("marimay-native", "go", "rust")
            )
            cells += [
                (
                    "noisy; repeat"
                    if noisy
                    else (
                        ("within target" if go_ratio <= target else "above target")
                        if target
                        else "measured"
                    )
                )
            ]
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        "## Dispersion",
        "",
        "| Workload | Engine | MAD ms | IQR ms | Min–max ms | Noise |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for identifier, row in result["workloads"].items():
        for p in participants:
            s = row["summary"][p]
            if s is None:
                continue
            lines.append(
                f"| {identifier} | {LABELS[p]} | {s['mad_ms']:.2f} | {s['iqr_ms']:.2f} | {s['min_ms']:.2f}–{s['max_ms']:.2f} | {s['noise_fraction']:.0%} |"
            )
    failures = [
        (w, p, outcome["error"])
        for w, row in result["workloads"].items()
        for p, outcome in row["outcomes"].items()
        if outcome["status"] == "failed"
    ]
    if failures:
        lines += [
            "",
            "## Failed cells",
            "",
            "The first failed observation is retained; remaining scheduled runs of that cell are marked skipped. Successful observations before a failure remain in JSON but have no summary or ratio.",
            "",
        ]
        for workload, participant, error in failures:
            lines += [
                f"### {workload} / {LABELS[participant]}",
                "",
                "```text",
                error,
                "```",
                "",
            ]
    lines += ["", "## Coverage and representations", ""]
    for identifier, row in result["workloads"].items():
        lines.append(f"- **{identifier}**: {row['description']}")
    lines += ["", "## Interpretation limits", ""]
    lines += ["- " + item for item in meta["limitations"]]
    lines += [
        "- The per-workload Go targets are exploratory thresholds, not reviewed release budgets. No average score or general ‘Go parity’ verdict is computed.",
        "- Short cases can be dominated by process startup and validation; repeat with larger documented inputs before attributing a difference to dispatch, GC or a particular primitive.",
        "- Interface results include array construction/boxing and compiler devirtualization opportunities; they are not isolated virtual-call latency.",
        "",
        "## Toolchains",
        "",
    ]
    lines += [f"- {name}: `{version}`" for name, version in meta["toolchains"].items()]
    lines += ["", f"Command: `{meta['command']}`", ""]
    return "\n".join(lines)
