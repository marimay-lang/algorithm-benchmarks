export interface Edge {
  to: number;
  weight: number;
}

export function bfs(adjacency: number[][], start: number): number[] | undefined {
  if (start < 0 || start >= adjacency.length) {
    return undefined;
  }
  const distances = new Array<number>(adjacency.length).fill(-1);
  const queue = new Array<number>(adjacency.length);
  let head = 0;
  let tail = 0;
  distances[start] = 0;
  queue[tail] = start;
  tail += 1;
  while (head < tail) {
    const node = queue[head];
    head += 1;
    for (const next of adjacency[node]) {
      if (next < 0 || next >= adjacency.length) {
        return undefined;
      }
      if (distances[next] === -1) {
        distances[next] = distances[node] + 1;
        queue[tail] = next;
        tail += 1;
      }
    }
  }
  return distances;
}

export function dijkstra(
  adjacency: Edge[][],
  start: number,
): number[] | undefined {
  if (start < 0 || start >= adjacency.length) {
    return undefined;
  }
  const distances = new Array<number>(adjacency.length).fill(1_000_000_000);
  const visited = new Array<boolean>(adjacency.length).fill(false);
  distances[start] = 0;
  for (let step = 0; step < adjacency.length; step += 1) {
    let best = -1;
    for (let node = 0; node < adjacency.length; node += 1) {
      if (!visited[node] && (best === -1 || distances[node] < distances[best])) {
        best = node;
      }
    }
    if (best === -1 || distances[best] === 1_000_000_000) {
      break;
    }
    visited[best] = true;
    for (const edge of adjacency[best]) {
      if (edge.to < 0 || edge.to >= adjacency.length || edge.weight < 0) {
        return undefined;
      }
      const candidate = distances[best] + edge.weight;
      if (candidate < distances[edge.to]) {
        distances[edge.to] = candidate;
      }
    }
  }
  return distances;
}
