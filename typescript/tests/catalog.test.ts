import { expect, test } from "bun:test";
import { Book, byteLength, stateFor, stateScore } from "../src/catalog/model";
import { parseDecimal } from "../src/catalog/objects";
import { runCatalog } from "../src/catalog/main";

test("UTF-8 byte lengths include non-BMP code points", () => {
  expect(byteLength("東京 🚀")).toBe(11);
  expect(byteLength("Война и мир")).toBe(20);
  expect(byteLength("🚀🙂")).toBe(8);
});
test("decimal parsing rejects partial and non-decimal values", () => {
  for (const token of ["12x", "", " ", "1e2", "0x10", "1.5", "1\n", "9007199254740993"]) {
    expect(parseDecimal(token).ok).toBe(false);
  }
  expect(parseDecimal("+123")).toEqual({ ok: true, value: 123 });
  expect(parseDecimal("-17")).toEqual({ ok: true, value: -17 });
});
test("fresh records share values and retain distinct identity", () => {
  const book = new Book("Книга", stateFor(1), 1);
  const copy = new Book(book.title, book.state, book.serial);
  expect(copy).not.toBe(book);
  expect(copy.state).toBe(book.state);
  expect(stateScore(copy.state)).toBe(3);
  expect(runCatalog("record-reference-copy", 17, 3) - runCatalog("record-create", 17, 3)).toBe(51);
});
