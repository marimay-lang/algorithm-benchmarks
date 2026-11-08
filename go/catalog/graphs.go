package catalog

type node struct {
	id        int
	neighbors []int
}

func BFS(n, rounds int, records bool) int {
	graph := [][]int{}
	nodes := []*node{}
	for i := 0; i < n; i++ {
		edges := []int{}
		for e := 1; e < 17; e++ {
			edges = append(edges, (i+e*e)%n)
		}
		graph = append(graph, edges)
		if records {
			nodes = append(nodes, &node{i, edges})
		}
	}
	c := 0
	for r := 0; r < rounds; r++ {
		distances := []int{}
		for i := 0; i < n; i++ {
			distances = append(distances, -1)
		}
		distances[0] = 0
		queue := []int{}
		objects := []*node{}
		if records {
			objects = append(objects, nodes[0])
		} else {
			queue = append(queue, 0)
		}
		for head := 0; head < n; head++ {
			index := 0
			edges := graph[0]
			if records {
				index = objects[head].id
				edges = objects[head].neighbors
			} else {
				index = queue[head]
				edges = graph[index]
			}
			for _, neighbor := range edges {
				if distances[neighbor] == -1 {
					distances[neighbor] = distances[index] + 1
					if records {
						objects = append(objects, nodes[neighbor])
					} else {
						queue = append(queue, neighbor)
					}
				}
			}
		}
		for i, d := range distances {
			c = add(c, (i+1)*(d+1))
		}
	}
	return c
}
