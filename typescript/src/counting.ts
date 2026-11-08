// Unicode scalar arrays use numeric code points, like Go rune and Rust char.
export function frequencies(values: number[]): Map<number, number> {
  const counts = new Map<number, number>();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return counts;
}
export function uniqueIntCount(values: number[]): number {
  const unique = new Set<number>();
  for (const value of values) unique.add(value);
  return unique.size;
}
