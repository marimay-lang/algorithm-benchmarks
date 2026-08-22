import { bfs, dijkstra, type Edge } from "./graphs";
import { heapSort, insertionSort } from "./sorting";
import { Dsu, MinHeap, Queue, Stack } from "./structures";

const CHECKSUM_MOD = 1_000_000_007;

function generatedValues(size: number, seed: number): number[] {
  const values = new Array<number>(size);
  let state = seed;
  for (let index = 0; index < size; index += 1) {
    state = (state * 25_173 + 13_849) % 65_536;
    values[index] = (state % 20_001) - 10_000;
  }
  return values;
}

function addChecksum(checksum: number, value: number): number {
  const normalized = ((value % CHECKSUM_MOD) + CHECKSUM_MOD) % CHECKSUM_MOD;
  return (checksum + normalized) % CHECKSUM_MOD;
}

function benchmarkInsertion(): number {
  let checksum = 0;
  for (let repeat = 0; repeat < 50; repeat += 1) {
    const values = generatedValues(2_500, repeat + 1);
    insertionSort(values);
    checksum = addChecksum(checksum, values[0]);
    checksum = addChecksum(checksum, values[Math.floor(values.length / 2)]);
    checksum = addChecksum(checksum, values[values.length - 1]);
  }
  return checksum;
}

function benchmarkHeapSort(): number {
  let checksum = 0;
  for (let repeat = 0; repeat < 5; repeat += 1) {
    const values = generatedValues(100_000, repeat + 101);
    heapSort(values);
    checksum = addChecksum(checksum, values[0]);
    checksum = addChecksum(checksum, values[Math.floor(values.length / 2)]);
    checksum = addChecksum(checksum, values[values.length - 1]);
  }
  return checksum;
}

function benchmarkStack(): number {
  const stack = new Stack();
  let state = 7;
  let checksum = 0;
  for (let index = 0; index < 1_000_000; index += 1) {
    state = (state * 25_173 + 13_849) % 65_536;
    stack.push(state % 1_001);
  }
  while (!stack.empty()) {
    checksum = addChecksum(checksum, stack.pop() as number);
  }
  return checksum;
}

function benchmarkQueue(): number {
  const queue = new Queue();
  let state = 11;
  let checksum = 0;
  for (let index = 0; index < 1_000_000; index += 1) {
    state = (state * 25_173 + 13_849) % 65_536;
    queue.enqueue(state % 1_001);
  }
  while (!queue.empty()) {
    checksum = addChecksum(checksum, queue.dequeue() as number);
  }
  return checksum;
}

function benchmarkMinHeap(): number {
  const heap = new MinHeap();
  let state = 13;
  let checksum = 0;
  for (let index = 0; index < 500_000; index += 1) {
    state = (state * 25_173 + 13_849) % 65_536;
    heap.push(state % 10_001);
  }
  while (!heap.empty()) {
    checksum = addChecksum(checksum, heap.pop() as number);
  }
  return checksum;
}

function benchmarkDsu(): number {
  const size = 100_000;
  const dsu = new Dsu(size);
  for (let operation = 0; operation < 5_000_000; operation += 1) {
    dsu.union(operation % size, (operation * 17 + 3) % size);
  }
  let checksum = dsu.components();
  for (let index = 0; index < size; index += 97) {
    checksum = addChecksum(checksum, dsu.find(index));
  }
  return checksum;
}

function benchmarkBfs(): number {
  const size = 20_000;
  const adjacency = Array.from({ length: size }, (_, node) => [
    (node + 1) % size,
    (node + size - 1) % size,
    (node + 7) % size,
    (node + size - 7) % size,
  ]);
  let checksum = 0;
  for (let repeat = 0; repeat < 300; repeat += 1) {
    const distances = bfs(adjacency, repeat);
    if (distances === undefined) {
      throw new Error("valid BFS input rejected");
    }
    checksum = addChecksum(checksum, distances[(repeat + Math.floor(size / 2)) % size]);
    checksum = addChecksum(checksum, distances[(repeat + Math.floor(size / 3)) % size]);
  }
  return checksum;
}

function benchmarkDijkstra(): number {
  const size = 800;
  const adjacency = Array.from({ length: size }, (_, node): Edge[] => {
    const edges: Edge[] = [];
    if (node + 1 < size) {
      edges.push({ to: node + 1, weight: 1 });
    }
    if (node + 7 < size) {
      edges.push({ to: node + 7, weight: 3 });
    }
    return edges;
  });
  let checksum = 0;
  for (let repeat = 0; repeat < 80; repeat += 1) {
    const distances = dijkstra(adjacency, repeat);
    if (distances === undefined) {
      throw new Error("valid Dijkstra input rejected");
    }
    checksum = addChecksum(checksum, distances[size - 1]);
    checksum = addChecksum(checksum, distances[size / 2]);
  }
  return checksum;
}

const name = Bun.argv[2];
const benchmarks: Record<string, () => number> = {
  insertion: benchmarkInsertion,
  "heap-sort": benchmarkHeapSort,
  stack: benchmarkStack,
  queue: benchmarkQueue,
  "min-heap": benchmarkMinHeap,
  dsu: benchmarkDsu,
  bfs: benchmarkBfs,
  dijkstra: benchmarkDijkstra,
};
const benchmark = benchmarks[name];
if (benchmark === undefined) {
  console.error(
    "usage: benchmark <insertion|heap-sort|stack|queue|min-heap|dsu|bfs|dijkstra>",
  );
  process.exit(2);
}
console.log(`${name} ${benchmark()}`);
