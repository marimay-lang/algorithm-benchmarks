package graphs

type Edge struct {
	To     int
	Weight int
}

func Dijkstra(adjacency [][]Edge, start int) ([]int, bool) {
	if start < 0 || start >= len(adjacency) {
		return nil, false
	}
	const infinity = 1_000_000_000
	distances := make([]int, len(adjacency))
	visited := make([]bool, len(adjacency))
	for index := range distances {
		distances[index] = infinity
	}
	distances[start] = 0
	for range adjacency {
		selected := -1
		for node := range adjacency {
			if !visited[node] && distances[node] < infinity && (selected == -1 || distances[node] < distances[selected]) {
				selected = node
			}
		}
		if selected == -1 {
			return distances, true
		}
		visited[selected] = true
		for _, edge := range adjacency[selected] {
			if edge.To < 0 || edge.To >= len(adjacency) || edge.Weight < 0 {
				return nil, false
			}
			candidate := distances[selected] + edge.Weight
			if candidate < distances[edge.To] {
				distances[edge.To] = candidate
			}
		}
	}
	return distances, true
}
