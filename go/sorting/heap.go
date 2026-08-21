package sorting

func siftDown(values []int, start, size int) {
	root := start
	for root*2+1 < size {
		left := root*2 + 1
		right := left + 1
		largest := left
		if right < size && values[right] > values[left] {
			largest = right
		}
		if values[root] >= values[largest] {
			return
		}
		values[root], values[largest] = values[largest], values[root]
		root = largest
	}
}

func HeapSort(values []int) {
	size := len(values)
	if size < 2 {
		return
	}
	for root := size / 2; root > 0; {
		root--
		siftDown(values, root, size)
	}
	for end := size - 1; end > 0; end-- {
		values[0], values[end] = values[end], values[0]
		siftDown(values, 0, end)
	}
}
