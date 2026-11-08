import { arrayGrowth, mapBook, mapInt, mapString, setChurn } from "./collections";
import { bfs } from "./graphs";
import { catalogPipeline, catalogWalk, parseResults, recordCopies } from "./objects";
import { normalizeTitle, report, titleSearch, wordFrequency } from "./text";

export function runCatalog(name: string, n: number, rounds: number): number {
  switch (name) {
    case "title-search-10k": return titleSearch(n, rounds);
    case "title-search-100k": return titleSearch(n, rounds);
    case "normalize-title": return normalizeTitle(n, rounds);
    case "word-frequency": return wordFrequency(n, rounds);
    case "report-builder": return report(n, rounds, true);
    case "report-concat": return report(n, rounds, false);
    case "map-int": return mapInt(n, rounds);
    case "map-string": return mapString(n, rounds);
    case "map-string-book": return mapBook(n, rounds);
    case "set-string-churn": return setChurn(n, rounds);
    case "catalog-match": return catalogWalk(n, rounds, 0);
    case "catalog-dotcall": return catalogWalk(n, rounds, 1);
    case "catalog-interface": return catalogWalk(n, rounds, 2);
    case "record-reference-copy": return recordCopies(n, rounds, false);
    case "record-create": return recordCopies(n, rounds, true);
    case "array-grow": return arrayGrowth(n, rounds, false);
    case "array-reserved": return arrayGrowth(n, rounds, true);
    case "bfs-int": return bfs(n, rounds, false);
    case "bfs-record": return bfs(n, rounds, true);
    case "catalog-pipeline": return catalogPipeline(n, rounds);
    case "parse-result": return parseResults(n, rounds);
    default: throw new Error(`unknown workload: ${name}`);
  }
}
function positive(s: string): number {
  if (!/^[0-9]+$/.test(s)) throw new Error("invalid argument");
  const value = Number(s);
  if (!Number.isSafeInteger(value) || value < 1 || value > 1_000_000) throw new Error("argument outside 1..1000000");
  return value;
}
if (import.meta.main) {
  if (Bun.argv.length !== 5) throw new Error("usage: catalog WORKLOAD SIZE ROUNDS");
  const [name, size, repeats] = Bun.argv.slice(2);
  const n = positive(size), rounds = positive(repeats);
  if (n * rounds > 20_000_000) throw new Error("operation count exceeds contract");
  console.log(`${name} ${runCatalog(name, n, rounds)}`);
}
