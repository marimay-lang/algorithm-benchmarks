module sorting

pub fn insertion_sort(mut values []int) {
	for index := 1; index < values.len; index++ {
		value := values[index]
		mut position := index
		for position > 0 && values[position - 1] > value {
			values[position] = values[position - 1]
			position--
		}
		values[position] = value
	}
}

fn sift_down(mut values []int, root int, size int) {
	mut current := root
	for {
		left := current * 2 + 1
		if left >= size {
			return
		}
		right := left + 1
		mut largest := left
		if right < size && values[right] > values[left] {
			largest = right
		}
		if values[current] >= values[largest] {
			return
		}
		values[current], values[largest] = values[largest], values[current]
		current = largest
	}
}

pub fn heap_sort(mut values []int) {
	for root := values.len / 2 - 1; root >= 0; root-- {
		sift_down(mut values, root, values.len)
	}
	for end := values.len - 1; end > 0; end-- {
		values[0], values[end] = values[end], values[0]
		sift_down(mut values, 0, end)
	}
}
