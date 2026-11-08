"""Keep failed cells visible while completing the balanced matrix schedule."""

from perf_protocol import ProtocolError, schedule


def measure_catalog(
    commands, expected, participants, workloads, warmups, samples, timed,
    progress=None, observed=None
):
    raw = {w: {p: [] for p in participants} for w in workloads}
    outcomes = {w: {p: {"status": "passed"} for p in participants} for w in workloads}
    events = schedule(workloads, participants, warmups, samples)
    round_size = len(participants) * len(workloads)
    for index, event in enumerate(events):
        if progress and index and index % round_size == 0:
            progress(index // round_size, warmups + samples)
        workload, participant = event["workload"], event["participant"]
        if outcomes[workload][participant]["status"] == "failed":
            event["status"] = "skipped-after-failure"
            if observed:
                observed(event)
            continue
        try:
            elapsed = timed(commands[participant][workload], expected[workload])
        except (ProtocolError, OSError) as error:
            event.update(status="failed", error=str(error))
            outcomes[workload][participant] = {"status": "failed", "error": str(error)}
            if observed:
                observed(event)
            print(f"FAILED {workload} / {participant}: {error}", flush=True)
            continue
        event.update(status="passed", elapsed_ms=elapsed)
        if event["phase"] == "sample":
            raw[workload][participant].append(elapsed)
        if observed:
            observed(event)
    if progress:
        progress(warmups + samples, warmups + samples)
    return raw, events, outcomes
