import { add } from "./model";

interface Node { id: number; neighbors: number[] }
export function bfs(n: number, rounds: number, records: boolean): number {
  const graph: number[][] = [];
  const nodes: Node[] = [];
  for (let i = 0; i < n; i++) {
    const edges: number[] = [];
    for (let e = 1; e < 17; e++) edges.push((i + e * e) % n);
    graph.push(edges);
    if (records) nodes.push({ id: i, neighbors: edges });
  }
  let c = 0;
  for (let r = 0; r < rounds; r++) {
    const distances: number[] = [];
    for (let i = 0; i < n; i++) distances.push(-1);
    distances[0] = 0;
    const queue: number[] = [];
    const objects: Node[] = [];
    if (records) objects.push(nodes[0]);
    else queue.push(0);
    for (let head = 0; head < n; head++) {
      const index = records ? objects[head].id : queue[head];
      const edges = records ? objects[head].neighbors : graph[index];
      for (const neighbor of edges) {
        if (distances[neighbor] === -1) {
          distances[neighbor] = distances[index] + 1;
          if (records) objects.push(nodes[neighbor]);
          else queue.push(neighbor);
        }
      }
    }
    for (let i = 0; i < n; i++) c = add(c, (i + 1) * (distances[i] + 1));
  }
  return c;
}
