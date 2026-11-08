import { Buffer } from "node:buffer";

export type BookState =
  | { tag: "available" }
  | { tag: "loaned"; days: number }
  | { tag: "lost" };
export interface Labelled { label(): string }
export class Book implements Labelled {
  constructor(public title: string, public state: BookState, public serial: number) {}
  label(): string { return this.title; }
}
export function stateFor(i: number): BookState {
  switch (i % 3) {
    case 0: return { tag: "available" };
    case 1: return { tag: "loaned", days: i % 97 };
    default: return { tag: "lost" };
  }
}
export function stateScore(state: BookState): number {
  switch (state.tag) {
    case "available": return 1;
    case "loaned": return state.days + 2;
    case "lost": return 101;
    default: return unreachable(state);
  }
}
function unreachable(value: never): never { throw new Error(`invalid state: ${value}`); }
export function titles(): string[] {
  return ["Война и мир", "Мастер и Маргарита", "Ёжик в тумане", "Книга моря",
    "Белый парус", "Путь домой", "Сад камней", "Зимняя ночь", "The Go Book",
    "Rust in Action", "Marimay λ", "東京 🚀", "Книга памяти", "Дальний берег",
    "Тихий Дон", "Алые паруса"];
}
export function titleFor(i: number, names: string[]): string {
  return `${names[i % names.length]} #${i}`;
}
export function books(n: number): Book[] {
  const names = titles();
  const values: Book[] = [];
  for (let i = 0; i < n; i++) values.push(new Book(names[i % names.length], stateFor(i), i));
  return values;
}
export function add(c: number, value: number): number { return (c + value) % 1_000_000_007; }
// The shared contract counts UTF-8 bytes, not JavaScript UTF-16 code units.
export function byteLength(s: string): number { return Buffer.byteLength(s, "utf8"); }
export function bytesChecksum(s: string): number {
  const bytes = new TextEncoder().encode(s);
  let c = 0;
  for (let i = 0; i < bytes.length; i++) c = add(c, (i % 251 + 1) * bytes[i]);
  return c;
}
