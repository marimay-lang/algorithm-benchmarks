pub fn bfs(adjacency: &[Vec<usize>], start: usize) -> Option<Vec<i64>> {
    if start >= adjacency.len() {
        return None;
    }
    let mut distances = vec![-1; adjacency.len()];
    let mut queue = vec![start];
    distances[start] = 0;
    let mut head = 0;
    while head < queue.len() {
        let node = queue[head];
        head += 1;
        for &neighbor in &adjacency[node] {
            if neighbor >= adjacency.len() {
                return None;
            }
            if distances[neighbor] == -1 {
                distances[neighbor] = distances[node] + 1;
                queue.push(neighbor);
            }
        }
    }
    Some(distances)
}
