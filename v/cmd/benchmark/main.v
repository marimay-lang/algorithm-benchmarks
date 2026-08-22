module main

import graphs
import os
import sorting
import structures

const checksum_mod = 1_000_000_007

fn generated_values(size int, seed int) []int {
	mut values := []int{len: size}
	mut state := seed
	for index in 0 .. size {
		state = (state * 25_173 + 13_849) % 65_536
		values[index] = state % 20_001 - 10_000
	}
	return values
}

fn add_checksum(checksum int, source_value int) int {
	mut value := source_value % checksum_mod
	if value < 0 {
		value += checksum_mod
	}
	return (checksum + value) % checksum_mod
}

fn benchmark_insertion() int {
	mut checksum := 0
	for repeat in 0 .. 50 {
		mut values := generated_values(2_500, repeat + 1)
		sorting.insertion_sort(mut values)
		checksum = add_checksum(checksum, values[0])
		checksum = add_checksum(checksum, values[values.len / 2])
		checksum = add_checksum(checksum, values[values.len - 1])
	}
	return checksum
}

fn benchmark_heap_sort() int {
	mut checksum := 0
	for repeat in 0 .. 5 {
		mut values := generated_values(100_000, repeat + 101)
		sorting.heap_sort(mut values)
		checksum = add_checksum(checksum, values[0])
		checksum = add_checksum(checksum, values[values.len / 2])
		checksum = add_checksum(checksum, values[values.len - 1])
	}
	return checksum
}

fn benchmark_stack() int {
	mut stack := structures.Stack{}
	mut state := 7
	mut checksum := 0
	for _ in 0 .. 1_000_000 {
		state = (state * 25_173 + 13_849) % 65_536
		stack.push(state % 1_001)
	}
	for !stack.empty() {
		checksum = add_checksum(checksum, stack.pop() or { panic('non-empty stack') })
	}
	return checksum
}

fn benchmark_queue() int {
	mut queue := structures.Queue{}
	mut state := 11
	mut checksum := 0
	for _ in 0 .. 1_000_000 {
		state = (state * 25_173 + 13_849) % 65_536
		queue.enqueue(state % 1_001)
	}
	for !queue.empty() {
		checksum = add_checksum(checksum, queue.dequeue() or { panic('non-empty queue') })
	}
	return checksum
}

fn benchmark_min_heap() int {
	mut heap := structures.MinHeap{}
	mut state := 13
	mut checksum := 0
	for _ in 0 .. 500_000 {
		state = (state * 25_173 + 13_849) % 65_536
		heap.push(state % 10_001)
	}
	for !heap.empty() {
		checksum = add_checksum(checksum, heap.pop() or { panic('non-empty heap') })
	}
	return checksum
}

fn benchmark_dsu() int {
	size := 100_000
	mut dsu := structures.new_dsu(size)
	for operation in 0 .. 5_000_000 {
		dsu.union(operation % size, (operation * 17 + 3) % size)
	}
	mut checksum := dsu.component_count()
	for index := 0; index < size; index += 97 {
		checksum = add_checksum(checksum, dsu.find(index))
	}
	return checksum
}

fn benchmark_bfs() int {
	size := 20_000
	mut adjacency := [][]int{len: size}
	for node in 0 .. size {
		adjacency[node] = [
			(node + 1) % size,
			(node + size - 1) % size,
			(node + 7) % size,
			(node + size - 7) % size,
		]
	}
	mut checksum := 0
	for repeat in 0 .. 300 {
		distances := graphs.bfs(adjacency, repeat) or { panic('valid BFS input rejected') }
		checksum = add_checksum(checksum, distances[(repeat + size / 2) % size])
		checksum = add_checksum(checksum, distances[(repeat + size / 3) % size])
	}
	return checksum
}

fn benchmark_dijkstra() int {
	size := 800
	mut adjacency := [][]graphs.Edge{len: size}
	for node in 0 .. size {
		mut edges := []graphs.Edge{cap: 2}
		if node + 1 < size {
			edges << graphs.Edge{
				to:     node + 1
				weight: 1
			}
		}
		if node + 7 < size {
			edges << graphs.Edge{
				to:     node + 7
				weight: 3
			}
		}
		adjacency[node] = edges
	}
	mut checksum := 0
	for repeat in 0 .. 80 {
		distances := graphs.dijkstra(adjacency, repeat) or {
			panic('valid Dijkstra input rejected')
		}
		checksum = add_checksum(checksum, distances[size - 1])
		checksum = add_checksum(checksum, distances[size / 2])
	}
	return checksum
}

fn main() {
	if os.args.len != 2 {
		eprintln('usage: benchmark <insertion|heap-sort|stack|queue|min-heap|dsu|bfs|dijkstra>')
		exit(2)
	}
	name := os.args[1]
	checksum := match name {
		'insertion' {
			benchmark_insertion()
		}
		'heap-sort' {
			benchmark_heap_sort()
		}
		'stack' {
			benchmark_stack()
		}
		'queue' {
			benchmark_queue()
		}
		'min-heap' {
			benchmark_min_heap()
		}
		'dsu' {
			benchmark_dsu()
		}
		'bfs' {
			benchmark_bfs()
		}
		'dijkstra' {
			benchmark_dijkstra()
		}
		else {
			eprintln('unknown benchmark: ${name}')
			exit(2)
		}
	}
	println('${name} ${checksum}')
}
