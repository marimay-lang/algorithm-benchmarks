package structures

type MinHeap struct {
	values []int
}

func NewMinHeap() *MinHeap {
	return &MinHeap{}
}

func (heap *MinHeap) Push(value int) {
	heap.values = append(heap.values, value)
	index := len(heap.values) - 1
	for index > 0 {
		parent := (index - 1) / 2
		if heap.values[parent] <= heap.values[index] {
			return
		}
		heap.values[parent], heap.values[index] = heap.values[index], heap.values[parent]
		index = parent
	}
}

func (heap *MinHeap) Pop() (int, bool) {
	if len(heap.values) == 0 {
		return 0, false
	}
	minimum := heap.values[0]
	last := len(heap.values) - 1
	heap.values[0] = heap.values[last]
	heap.values = heap.values[:last]
	heap.siftDown(0)
	return minimum, true
}

func (heap *MinHeap) Peek() (int, bool) {
	if len(heap.values) == 0 {
		return 0, false
	}
	return heap.values[0], true
}

func (heap *MinHeap) Len() int {
	return len(heap.values)
}

func (heap *MinHeap) Empty() bool {
	return len(heap.values) == 0
}

func (heap *MinHeap) siftDown(start int) {
	index := start
	for index*2+1 < len(heap.values) {
		left := index*2 + 1
		right := left + 1
		smallest := left
		if right < len(heap.values) && heap.values[right] < heap.values[left] {
			smallest = right
		}
		if heap.values[index] <= heap.values[smallest] {
			return
		}
		heap.values[index], heap.values[smallest] = heap.values[smallest], heap.values[index]
		index = smallest
	}
}
