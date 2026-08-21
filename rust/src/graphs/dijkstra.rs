#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Edge {
    pub to: usize,
    pub weight: i64,
}

pub fn dijkstra(adjacency: &[Vec<Edge>], start: usize) -> Option<Vec<i64>> {
    if start >= adjacency.len() {
        return None;
    }
    const INFINITY: i64 = 1_000_000_000;
    let mut distances = vec![INFINITY; adjacency.len()];
    let mut visited = vec![false; adjacency.len()];
    distances[start] = 0;
    for _ in adjacency {
        let selected = (0..adjacency.len())
            .filter(|&node| !visited[node] && distances[node] < INFINITY)
            .min_by_key(|&node| distances[node]);
        let Some(selected) = selected else {
            return Some(distances);
        };
        visited[selected] = true;
        for edge in &adjacency[selected] {
            if edge.to >= adjacency.len() || edge.weight < 0 {
                return None;
            }
            let candidate = distances[selected] + edge.weight;
            if candidate < distances[edge.to] {
                distances[edge.to] = candidate;
            }
        }
    }
    Some(distances)
}
