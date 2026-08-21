package sorting

func InsertionSort(values []int) {
	for index := 1; index < len(values); index++ {
		current := values[index]
		position := index
		for position > 0 && values[position-1] > current {
			values[position] = values[position-1]
			position--
		}
		values[position] = current
	}
}
