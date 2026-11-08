import { Book, add, byteLength, stateFor, stateScore, titleFor, titles } from "./model";

export function mapInt(n: number, rounds: number): number {
  const counts = new Map<number, number>();
  for (let i = 0; i < n * rounds; i++) {
    const key = (i * 25173 + 13849) % n;
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  let c = counts.size;
  for (let k = 0; k < n; k++) c = add(c, (k + 1) * (counts.get(k) ?? 0));
  return c;
}
export function mapString(n: number, rounds: number): number {
  const names = titles();
  const keys: string[] = [];
  for (let i = 0; i < n; i++) keys.push(titleFor(i, names));
  const counts = new Map<string, number>();
  for (let i = 0; i < n * rounds; i++) {
    const key = keys[(i * 25173 + 13849) % n];
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  let c = counts.size;
  for (let i = 0; i < n; i++) c = add(c, (i + 1) * (counts.get(titleFor(i, names)) ?? 0));
  return c;
}
export function mapBook(n: number, rounds: number): number {
  const names = titles();
  const values = new Map<string, Book>();
  for (let i = 0; i < n; i++) {
    const name = titleFor(i, names);
    values.set(name, new Book(name, stateFor(i), i));
  }
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    for (let i = 0; i < n; i++) {
      const b = values.get(titleFor(i, names));
      if (b === undefined) throw new Error("missing book");
      c = add(c, byteLength(b.title) + stateScore(b.state) + b.serial);
    }
  }
  return c;
}
export function setChurn(n: number, rounds: number): number {
  const names = titles();
  const values = new Set<string>();
  for (let i = 0; i < n; i++) values.add(titleFor(i, names));
  let c = 0;
  for (let s = 0; s < n * rounds; s++) {
    const key = titleFor(s, names);
    if (!values.delete(key)) throw new Error("missing removal");
    if (values.has(titleFor(s, names))) throw new Error("removed key");
    values.add(titleFor(s + n, names));
    c = add(c, values.size);
  }
  for (let i = n * rounds; i < n * (rounds + 1); i++) {
    if (!values.has(titleFor(i, names))) throw new Error("missing final");
    c = add(c, byteLength(titleFor(i, names)));
  }
  return c;
}
export function arrayGrowth(n: number, rounds: number, reserved: boolean): number {
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    // JS has no reserve-only API: use a pre-sized Array and indexed writes.
    const values: number[] = reserved ? new Array<number>(n) : [];
    for (let i = 0; i < n; i++) {
      if (reserved) values[i] = i * 17 % 1009;
      else values.push(i * 17 % 1009);
    }
    for (const value of values) c = add(c, value);
  }
  return c;
}
