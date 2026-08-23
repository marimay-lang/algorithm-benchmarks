package main

import (
	"reflect"
	"testing"

	"example.com/marimay-algorithms/graphs"
	"example.com/marimay-algorithms/sorting"
	"example.com/marimay-algorithms/structures"
)

func TestSorting(t *testing.T) {
	insertionValues := []int{5, -1, 5, 3, 0}
	sorting.InsertionSort(insertionValues)
	if expected := []int{-1, 0, 3, 5, 5}; !reflect.DeepEqual(insertionValues, expected) {
		t.Fatalf("insertion sort: got %v, want %v", insertionValues, expected)
	}
	heapValues := []int{9, 4, 7, 1, -2, 6, 5}
	sorting.HeapSort(heapValues)
	if expected := []int{-2, 1, 4, 5, 6, 7, 9}; !reflect.DeepEqual(heapValues, expected) {
		t.Fatalf("heap sort: got %v, want %v", heapValues, expected)
	}
}

func TestStructures(t *testing.T) {
	stack := structures.NewStack()
	stack.Push(10)
	stack.Push(20)
	stack.Push(30)
	if value, ok := stack.Pop(); !ok || value != 30 {
		t.Fatalf("stack pop: got %d, %v", value, ok)
	}
	queue := structures.NewQueue()
	queue.Enqueue(10)
	queue.Enqueue(20)
	queue.Enqueue(30)
	if value, ok := queue.Dequeue(); !ok || value != 10 {
		t.Fatalf("queue dequeue: got %d, %v", value, ok)
	}
	heap := structures.NewMinHeap()
	for _, value := range []int{7, 2, 9, 1, 5} {
		heap.Push(value)
	}
	if value, ok := heap.Pop(); !ok || value != 1 {
		t.Fatalf("heap pop: got %d, %v", value, ok)
	}
	dsu := structures.NewDSU(6)
	dsu.Union(0, 1)
	dsu.Union(1, 2)
	dsu.Union(3, 4)
	if !dsu.Connected(0, 2) || dsu.Connected(0, 3) || dsu.Components() != 3 {
		t.Fatal("dsu invariants failed")
	}
}

func TestGraphs(t *testing.T) {
	unweighted := [][]int{{1, 2}, {0, 3}, {0, 3, 4}, {1, 2, 4}, {2, 3}}
	distances, ok := graphs.BFS(unweighted, 0)
	if expected := []int{0, 1, 1, 2, 2}; !ok || !reflect.DeepEqual(distances, expected) {
		t.Fatalf("bfs: got %v, %v; want %v", distances, ok, expected)
	}
	weighted := [][]graphs.Edge{
		{{To: 1, Weight: 4}, {To: 2, Weight: 1}},
		{{To: 3, Weight: 1}},
		{{To: 1, Weight: 2}, {To: 3, Weight: 5}},
		{{To: 4, Weight: 3}},
		{},
	}
	distances, ok = graphs.Dijkstra(weighted, 0)
	if expected := []int{0, 3, 1, 4, 7}; !ok || !reflect.DeepEqual(distances, expected) {
		t.Fatalf("dijkstra: got %v, %v; want %v", distances, ok, expected)
	}
}

func TestInvalidGraphInputs(t *testing.T) {
	if _, ok := graphs.BFS(nil, -1); ok {
		t.Fatal("BFS accepted an invalid start")
	}
	if _, ok := graphs.BFS([][]int{{1}, {2}}, 0); ok {
		t.Fatal("BFS accepted an out-of-range neighbor")
	}
	if _, ok := graphs.Dijkstra(nil, -1); ok {
		t.Fatal("Dijkstra accepted an invalid start")
	}
	if _, ok := graphs.Dijkstra([][]graphs.Edge{{{To: 2, Weight: 1}}, {}}, 0); ok {
		t.Fatal("Dijkstra accepted an out-of-range endpoint")
	}
	if _, ok := graphs.Dijkstra([][]graphs.Edge{{{To: 1, Weight: -1}}, {}}, 0); ok {
		t.Fatal("Dijkstra accepted a negative weight")
	}
}
