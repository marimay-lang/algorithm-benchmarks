package graphs

func BFS(adjacency [][]int, start int) ([]int, bool) {
	if start < 0 || start >= len(adjacency) {
		return nil, false
	}
	distances := make([]int, len(adjacency))
	for index := range distances {
		distances[index] = -1
	}
	queue := []int{start}
	distances[start] = 0
	for head := 0; head < len(queue); head++ {
		node := queue[head]
		for _, neighbor := range adjacency[node] {
			if neighbor < 0 || neighbor >= len(adjacency) {
				return nil, false
			}
			if distances[neighbor] == -1 {
				distances[neighbor] = distances[node] + 1
				queue = append(queue, neighbor)
			}
		}
	}
	return distances, true
}
