package main

import (
	"fmt"
	"os"

	"example.com/ruda-algorithms/graphs"
	"example.com/ruda-algorithms/sorting"
	"example.com/ruda-algorithms/structures"
)

const checksumMod = 1_000_000_007

func generatedValues(size, seed int) []int {
	values := make([]int, size)
	state := seed
	for index := range values {
		state = (state*25173 + 13849) % 65536
		values[index] = state%20001 - 10000
	}
	return values
}

func addChecksum(checksum, value int) int {
	value %= checksumMod
	if value < 0 {
		value += checksumMod
	}
	return (checksum + value) % checksumMod
}

func benchmarkInsertion() int {
	checksum := 0
	for repeat := 0; repeat < 50; repeat++ {
		values := generatedValues(2500, repeat+1)
		sorting.InsertionSort(values)
		checksum = addChecksum(checksum, values[0])
		checksum = addChecksum(checksum, values[len(values)/2])
		checksum = addChecksum(checksum, values[len(values)-1])
	}
	return checksum
}

func benchmarkHeapSort() int {
	checksum := 0
	for repeat := 0; repeat < 5; repeat++ {
		values := generatedValues(100_000, repeat+101)
		sorting.HeapSort(values)
		checksum = addChecksum(checksum, values[0])
		checksum = addChecksum(checksum, values[len(values)/2])
		checksum = addChecksum(checksum, values[len(values)-1])
	}
	return checksum
}

func benchmarkStack() int {
	stack := structures.NewStack()
	state := 7
	checksum := 0
	for index := 0; index < 1_000_000; index++ {
		state = (state*25173 + 13849) % 65536
		stack.Push(state % 1001)
	}
	for !stack.Empty() {
		value, _ := stack.Pop()
		checksum = addChecksum(checksum, value)
	}
	return checksum
}

func benchmarkQueue() int {
	queue := structures.NewQueue()
	state := 11
	checksum := 0
	for index := 0; index < 1_000_000; index++ {
		state = (state*25173 + 13849) % 65536
		queue.Enqueue(state % 1001)
	}
	for !queue.Empty() {
		value, _ := queue.Dequeue()
		checksum = addChecksum(checksum, value)
	}
	return checksum
}

func benchmarkMinHeap() int {
	heap := structures.NewMinHeap()
	state := 13
	checksum := 0
	for index := 0; index < 500_000; index++ {
		state = (state*25173 + 13849) % 65536
		heap.Push(state % 10001)
	}
	for !heap.Empty() {
		value, _ := heap.Pop()
		checksum = addChecksum(checksum, value)
	}
	return checksum
}

func benchmarkDSU() int {
	const size = 100_000
	dsu := structures.NewDSU(size)
	for operation := 0; operation < 5_000_000; operation++ {
		left := operation % size
		right := (operation*17 + 3) % size
		dsu.Union(left, right)
	}
	checksum := dsu.Components()
	for index := 0; index < size; index += 97 {
		checksum = addChecksum(checksum, dsu.Find(index))
	}
	return checksum
}

func benchmarkBFS() int {
	const size = 20_000
	adjacency := make([][]int, size)
	for node := 0; node < size; node++ {
		adjacency[node] = []int{
			(node + 1) % size,
			(node + size - 1) % size,
			(node + 7) % size,
			(node + size - 7) % size,
		}
	}
	checksum := 0
	for repeat := 0; repeat < 300; repeat++ {
		distances, ok := graphs.BFS(adjacency, repeat)
		if !ok {
			panic("valid BFS input rejected")
		}
		checksum = addChecksum(checksum, distances[(repeat+size/2)%size])
		checksum = addChecksum(checksum, distances[(repeat+size/3)%size])
	}
	return checksum
}

func benchmarkDijkstra() int {
	const size = 800
	adjacency := make([][]graphs.Edge, size)
	for node := 0; node < size; node++ {
		if node+1 < size {
			adjacency[node] = append(adjacency[node], graphs.Edge{To: node + 1, Weight: 1})
		}
		if node+7 < size {
			adjacency[node] = append(adjacency[node], graphs.Edge{To: node + 7, Weight: 3})
		}
	}
	checksum := 0
	for repeat := 0; repeat < 80; repeat++ {
		distances, ok := graphs.Dijkstra(adjacency, repeat)
		if !ok {
			panic("valid Dijkstra input rejected")
		}
		checksum = addChecksum(checksum, distances[size-1])
		checksum = addChecksum(checksum, distances[size/2])
	}
	return checksum
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: benchmark <insertion|heap-sort|stack|queue|min-heap|dsu|bfs|dijkstra>")
		os.Exit(2)
	}
	name := os.Args[1]
	benchmarks := map[string]func() int{
		"insertion": benchmarkInsertion,
		"heap-sort": benchmarkHeapSort,
		"stack":     benchmarkStack,
		"queue":     benchmarkQueue,
		"min-heap":  benchmarkMinHeap,
		"dsu":       benchmarkDSU,
		"bfs":       benchmarkBFS,
		"dijkstra":  benchmarkDijkstra,
	}
	benchmark, ok := benchmarks[name]
	if !ok {
		fmt.Fprintf(os.Stderr, "unknown benchmark: %s\n", name)
		os.Exit(2)
	}
	fmt.Printf("%s %d\n", name, benchmark())
}
