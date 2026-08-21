package main

import (
	"fmt"

	"example.com/ruda-algorithms/graphs"
	"example.com/ruda-algorithms/sorting"
	"example.com/ruda-algorithms/structures"
)

func main() {
	values := []int{5, 1, 4, 2, 3}
	sorting.HeapSort(values)
	heap := structures.NewMinHeap()
	heap.Push(3)
	heap.Push(1)
	distances, ok := graphs.BFS([][]int{{1}, {0, 2}, {1}}, 0)
	minimum, heapOK := heap.Pop()
	if values[0] != 1 || values[4] != 5 || !ok || distances[2] != 2 || !heapOK || minimum != 1 {
		panic("Go algorithms smoke test failed")
	}
	fmt.Println("Go algorithms: ok")
}
