///|
pub(all) struct Edge {
  to : Int
  weight : Int
}

///|
pub fn bfs(adjacency : Array[Array[Int]], start : Int) -> Array[Int]? {
  if start < 0 || start >= adjacency.length() {
    return None
  }
  let distances = Array::make(adjacency.length(), -1)
  let queue = Array::make(adjacency.length(), 0)
  let mut head = 0
  let mut tail = 0
  distances[start] = 0
  queue[tail] = start
  tail = tail + 1
  while head < tail {
    let node = queue[head]
    head = head + 1
    for next in adjacency[node] {
      if next < 0 || next >= adjacency.length() {
        return None
      }
      if distances[next] == -1 {
        distances[next] = distances[node] + 1
        queue[tail] = next
        tail = tail + 1
      }
    }
  }
  Some(distances)
}

///|
pub fn dijkstra(adjacency : Array[Array[Edge]], start : Int) -> Array[Int]? {
  if start < 0 || start >= adjacency.length() {
    return None
  }
  let distances = Array::make(adjacency.length(), 1_000_000_000)
  let visited = Array::make(adjacency.length(), false)
  distances[start] = 0
  for _step = 0; _step < adjacency.length(); _step = _step + 1 {
    let mut best = -1
    for node = 0; node < adjacency.length(); node = node + 1 {
      if !visited[node] && (best == -1 || distances[node] < distances[best]) {
        best = node
      }
    }
    if best == -1 || distances[best] == 1_000_000_000 {
      break
    }
    visited[best] = true
    for edge in adjacency[best] {
      if edge.to < 0 || edge.to >= adjacency.length() || edge.weight < 0 {
        return None
      }
      let candidate = distances[best] + edge.weight
      if candidate < distances[edge.to] {
        distances[edge.to] = candidate
      }
    }
  }
  Some(distances)
}
