module graphs

pub struct Edge {
pub:
	to     int
	weight int
}

pub fn bfs(adjacency [][]int, start int) ?[]int {
	if start < 0 || start >= adjacency.len {
		return none
	}
	mut distances := []int{len: adjacency.len, init: -1}
	mut queue := []int{len: adjacency.len}
	mut head := 0
	mut tail := 0
	distances[start] = 0
	queue[tail] = start
	tail++
	for head < tail {
		node := queue[head]
		head++
		for next in adjacency[node] {
			if next < 0 || next >= adjacency.len {
				return none
			}
			if distances[next] == -1 {
				distances[next] = distances[node] + 1
				queue[tail] = next
				tail++
			}
		}
	}
	return distances
}

pub fn dijkstra(adjacency [][]Edge, start int) ?[]int {
	if start < 0 || start >= adjacency.len {
		return none
	}
	mut distances := []int{len: adjacency.len, init: 1_000_000_000}
	mut visited := []bool{len: adjacency.len}
	distances[start] = 0
	for _ in 0 .. adjacency.len {
		mut best := -1
		for node in 0 .. adjacency.len {
			if !visited[node] && (best == -1 || distances[node] < distances[best]) {
				best = node
			}
		}
		if best == -1 || distances[best] == 1_000_000_000 {
			break
		}
		visited[best] = true
		for edge in adjacency[best] {
			if edge.to < 0 || edge.to >= adjacency.len || edge.weight < 0 {
				return none
			}
			candidate := distances[best] + edge.weight
			if candidate < distances[edge.to] {
				distances[edge.to] = candidate
			}
		}
	}
	return distances
}
