from __future__ import annotations

import unittest

from cp41_codegen import (
    generated_hot_symbols,
    parse_disassembly,
    parse_nm,
    select_hot_symbol,
    stack_addressed_operations,
)


class Checkpoint41CodegenTests(unittest.TestCase):
    def test_parses_generated_symbols_and_selects_text_only(self) -> None:
        symbols = parse_nm(
            "mmay_g_f_0123456789abcdef0123456789abcdef t 10 2a\n"
            "other_symbol t 40 90\n"
            "mmay_g_f_fedcba9876543210fedcba9876543210 d 80 12\n"
        )
        self.assertEqual(
            symbols, {"mmay_g_f_0123456789abcdef0123456789abcdef": 42}
        )

    def test_groups_symbolized_disassembly(self) -> None:
        functions = parse_disassembly(
            "0000 <mmay_g_f_0123456789abcdef0123456789abcdef>:\n"
            "  0: mov rax, qword ptr [rsp + 8]\n"
            "0010 <other_symbol>:\n"
            " 10: ret\n"
        )
        self.assertEqual(len(next(iter(functions.values()))), 1)

    def test_counts_stack_operands_for_both_targets(self) -> None:
        self.assertEqual(
            stack_addressed_operations(
                ["mov rax, [rsp + 8]", "mov [rbp-16], rcx", "mov rax, [rdi]"],
                "x86_64",
            ),
            2,
        )

    def test_selects_retained_core_or_inlined_entry(self) -> None:
        entry = "mmay_g_f_0123456789abcdef0123456789abcdef"
        core = "mmay_g_f_fedcba9876543210fedcba9876543210"
        source = (
            f"static int {core}(void);\n"
            f"static int {entry}(void) {{\n"
            f"  mmay_g_s = {core}(mmay_g_x, mmay_g_p);\n"
            "}\n"
            "int main(void) { "
            f"mmay_g_s = {entry}(&mmay_g_x, &mmay_g_p, &mmay_g_result, "
            "&mmay_g_start, &mmay_g_end); }\n"
        )
        self.assertEqual(generated_hot_symbols(source), (entry, core))
        self.assertEqual(
            select_hot_symbol({entry: 100, core: 80}, source),
            (core, entry, True),
        )
        self.assertEqual(
            select_hot_symbol({entry: 100}, source),
            (entry, entry, False),
        )
        self.assertEqual(
            stack_addressed_operations(
                ["ldr x0, [sp, #8]", "str x1, [x29]", "ldr x2, [x3]"],
                "arm64",
            ),
            2,
        )


if __name__ == "__main__":
    unittest.main()
