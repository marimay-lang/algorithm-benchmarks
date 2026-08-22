module structures

pub struct Stack {
mut:
	values []int
}

pub fn (mut stack Stack) push(value int) {
	stack.values << value
}

pub fn (mut stack Stack) pop() ?int {
	if stack.values.len == 0 {
		return none
	}
	return stack.values.pop()
}

pub fn (stack &Stack) empty() bool {
	return stack.values.len == 0
}

pub struct Queue {
mut:
	values []int
	head   int
}

pub fn (mut queue Queue) enqueue(value int) {
	queue.values << value
}

pub fn (mut queue Queue) dequeue() ?int {
	if queue.head >= queue.values.len {
		return none
	}
	value := queue.values[queue.head]
	queue.head++
	return value
}

pub fn (queue &Queue) empty() bool {
	return queue.head >= queue.values.len
}

pub struct MinHeap {
mut:
	values []int
}

pub fn (mut heap MinHeap) push(value int) {
	heap.values << value
	mut index := heap.values.len - 1
	for index > 0 {
		parent := (index - 1) / 2
		if heap.values[parent] <= heap.values[index] {
			return
		}
		heap.values[parent], heap.values[index] = heap.values[index], heap.values[parent]
		index = parent
	}
}

pub fn (mut heap MinHeap) pop() ?int {
	if heap.values.len == 0 {
		return none
	}
	result := heap.values[0]
	last := heap.values.pop()
	if heap.values.len == 0 {
		return result
	}
	heap.values[0] = last
	mut index := 0
	for {
		left := index * 2 + 1
		if left >= heap.values.len {
			break
		}
		right := left + 1
		mut smallest := left
		if right < heap.values.len && heap.values[right] < heap.values[left] {
			smallest = right
		}
		if heap.values[index] <= heap.values[smallest] {
			break
		}
		heap.values[index], heap.values[smallest] = heap.values[smallest], heap.values[index]
		index = smallest
	}
	return result
}

pub fn (heap &MinHeap) empty() bool {
	return heap.values.len == 0
}

pub struct Dsu {
mut:
	parent     []int
	rank       []int
	components int
}

pub fn new_dsu(size int) Dsu {
	mut parent := []int{len: size}
	for index in 0 .. size {
		parent[index] = index
	}
	return Dsu{
		parent:     parent
		rank:       []int{len: size}
		components: size
	}
}

pub fn (mut dsu Dsu) find(value int) int {
	mut root := value
	for dsu.parent[root] != root {
		root = dsu.parent[root]
	}
	mut current := value
	for dsu.parent[current] != current {
		next := dsu.parent[current]
		dsu.parent[current] = root
		current = next
	}
	return root
}

pub fn (mut dsu Dsu) union(left int, right int) {
	mut left_root := dsu.find(left)
	mut right_root := dsu.find(right)
	if left_root == right_root {
		return
	}
	if dsu.rank[left_root] < dsu.rank[right_root] {
		left_root, right_root = right_root, left_root
	}
	dsu.parent[right_root] = left_root
	if dsu.rank[left_root] == dsu.rank[right_root] {
		dsu.rank[left_root]++
	}
	dsu.components--
}

pub fn (dsu &Dsu) component_count() int {
	return dsu.components
}
