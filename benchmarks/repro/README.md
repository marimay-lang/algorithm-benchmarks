# VM repeated-concatenation diagnostic

`vm-concat.my` constructs 10,000 report rows using fresh immutable strings.
Expected stdout is exactly `178890\n`: the final value is 178,890 UTF-8 bytes.
This is a standalone diagnostic, outside the timed workload contract.

```sh
mmay run benchmarks/repro/vm-concat.my --engine vm --max-heap-bytes 67108864
mmay run benchmarks/repro/vm-concat.my --engine vm --max-heap-bytes 268435456
mmay run benchmarks/repro/vm-concat.my --engine native --max-heap-bytes 67108864
```

The corresponding full benchmark is:

```sh
mmay run marimay/catalog --engine vm --max-heap-bytes 67108864 -- report-concat 10000 1
```

It expects `report-concat 762303259\n`, checks every output byte, and creates
272,015 final UTF-8 bytes. `report-builder` constructs the same content with
`std/text.Builder` and expects `report-builder 762303259\n`.

Observed locally on 2026-09-09 with compiler SHA-256
`7da536ea73bfdec7809ee6369bc4839133fb99aff4adfc167635d47287c8b0be`:

| Execution | Exit | stdout | stderr |
|---|---:|---|---|
| VM, managed heap 64 MiB | 70 | empty | `I0002: VM execution failed a resource, integrity, or host requirement` |
| VM, managed heap 256 MiB | 70 | empty | same `I0002` |
| Native, default profile, managed heap 64 MiB | 0 | `178890\n` | empty |

Raising the managed heap did not resolve this observed case. A separate
`max_total_string_bytes` / `total_string_bytes` limit in VM interning is an
investigation lead, not a confirmed root-cause diagnosis. Re-run these commands
after a runtime fix; this table records one build, not a permanent limitation.
