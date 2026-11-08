import { Book, type Labelled, add, books, byteLength, stateScore, titles } from "./model";

function interfaceLabel(value: Labelled): string { return value.label(); }
export function catalogWalk(n: number, rounds: number, mode: number): number {
  const values = books(n);
  const labels: Labelled[] = [];
  if (mode === 2) for (const b of values) labels.push(b);
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    for (let i = 0; i < n; i++) {
      if (mode === 0) c = add(c, stateScore(values[i].state) + byteLength(values[i].title));
      if (mode === 1) c = add(c, byteLength(values[i].label()));
      if (mode === 2) c = add(c, byteLength(interfaceLabel(labels[i])));
    }
  }
  return c;
}
export function recordCopies(n: number, rounds: number, fresh: boolean): number {
  const original = books(n);
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    const retained: Book[] = [];
    for (const b of original) retained.push(fresh ? new Book(b.title, b.state, b.serial) : b);
    for (let i = 0; i < retained.length; i++) {
      const b = retained[i];
      c = add(c, b.serial + byteLength(b.title) + (original[i] === b ? 1 : 0));
    }
  }
  return c;
}
export function catalogPipeline(n: number, rounds: number): number {
  const values = books(n);
  const names = titles();
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    const counts = new Map<string, number>();
    for (const b of values) {
      counts.set(b.title, (counts.get(b.title) ?? 0) + 1);
      c = add(c, stateScore(b.state));
    }
    for (let q = 0; q < 64; q++) {
      const target = q % 4 === 3 ? "книги нет" : names[q % names.length];
      let found = 0;
      for (const b of values) {
        if (b.title === target) { found = b.serial + 1; break; }
      }
      c = add(c, found);
      c = add(c, counts.get(target) ?? 0);
    }
  }
  return c;
}
export type ParseResult = { ok: true; value: number } | { ok: false; error: "invalid" };
export function parseDecimal(s: string): ParseResult {
  if (!/^[+-]?[0-9]+$/.test(s)) return { ok: false, error: "invalid" };
  const value = Number(s);
  return Number.isSafeInteger(value) ? { ok: true, value } : { ok: false, error: "invalid" };
}
function parsedScore(s: string): ParseResult {
  const parsed = parseDecimal(s);
  if (!parsed.ok) return parsed;
  return { ok: true, value: parsed.value + 1 };
}
export function parseResults(n: number, rounds: number): number {
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    for (let i = 0; i < n; i++) {
      let token = `${i % 1009}`;
      if (i % 4 === 3) token += "x";
      const result = parsedScore(token);
      c = add(c, result.ok ? result.value : 7);
    }
  }
  return c;
}
