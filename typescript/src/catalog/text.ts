import { add, byteLength, bytesChecksum, titleFor, titles } from "./model";

export function titleSearch(n: number, rounds: number): number {
  const names = titles();
  const values: string[] = [];
  for (let i = 0; i < n; i++) values.push(titleFor(i, names));
  let c = 0;
  for (let q = 0; q < rounds; q++) {
    const target = q % 4 === 3 ? "книги нет" : titleFor(q * 7919 % n, names);
    let found = 0;
    for (let i = 0; i < values.length; i++) {
      if (values[i] === target) { found = i + 1; break; }
    }
    c = add(c, found);
  }
  return c;
}
export function normalizeTitle(n: number, rounds: number): number {
  const upper = Array.from("ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ");
  const lower = Array.from("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя");
  const folding = new Map<string, string>();
  for (let i = 0; i < upper.length; i++) folding.set(upper[i], lower[i]);
  const inputs = [" \tВОЙНА И МИР\r\n", "  ЁЖИК В ТУМАНЕ ", " THE GO BOOK\t", " МАСТЕР И МАРГАРИТА "];
  const expected = ["война и мир", "ёжик в тумане", "the go book", "мастер и маргарита"];
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    for (let i = 0; i < n; i++) {
      const pieces: string[] = [];
      const trimmed = inputs[i % 4].replace(/^[ \t\n\r\v\f]+|[ \t\n\r\v\f]+$/g, "");
      for (const s of Array.from(trimmed)) pieces.push(folding.get(s) ?? s);
      const out = pieces.join("");
      if (out !== expected[i % 4]) throw new Error("normalization");
      c = add(c, byteLength(out));
    }
  }
  return c;
}
export function wordFrequency(n: number, rounds: number): number {
  const lines = ["книга море книга дом", "море свет дом книга", "rust go marimay go", "ёжик туман ёжик книга"];
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    const counts = new Map<string, number>();
    for (let i = 0; i < n; i++) {
      const words = lines[i % 4].split(" ");
      for (const word of words) counts.set(word, (counts.get(word) ?? 0) + 1);
    }
    for (const word of ["книга", "море", "дом", "свет", "rust", "go", "marimay", "ёжик", "туман"]) {
      c = add(c, (counts.get(word) ?? 0) * byteLength(word));
    }
    c = add(c, counts.size);
  }
  return c;
}
export function report(n: number, rounds: number, builderMode: boolean): number {
  const names = titles();
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    const pieces: string[] = [];
    let result = "";
    for (let i = 0; i < n; i++) {
      const line = `${i}|${names[i % names.length]}|${i % 3}\n`;
      if (builderMode) pieces.push(line);
      else result = `${result}${line}`;
    }
    if (builderMode) result = pieces.join("");
    c = add(c, bytesChecksum(result));
  }
  return c;
}
