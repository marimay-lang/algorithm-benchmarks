package structures

type Queue struct {
	values []int
	head   int
}

func NewQueue() *Queue {
	return &Queue{}
}

func (queue *Queue) Enqueue(value int) {
	queue.values = append(queue.values, value)
}

func (queue *Queue) Dequeue() (int, bool) {
	if queue.head == len(queue.values) {
		return 0, false
	}
	value := queue.values[queue.head]
	queue.head++
	return value, true
}

func (queue *Queue) Front() (int, bool) {
	if queue.head == len(queue.values) {
		return 0, false
	}
	return queue.values[queue.head], true
}

func (queue *Queue) Len() int {
	return len(queue.values) - queue.head
}

func (queue *Queue) Empty() bool {
	return queue.head == len(queue.values)
}
