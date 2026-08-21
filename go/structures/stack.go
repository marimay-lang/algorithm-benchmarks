package structures

type Stack struct {
	values []int
}

func NewStack() *Stack {
	return &Stack{}
}

func (stack *Stack) Push(value int) {
	stack.values = append(stack.values, value)
}

func (stack *Stack) Pop() (int, bool) {
	if len(stack.values) == 0 {
		return 0, false
	}
	last := len(stack.values) - 1
	value := stack.values[last]
	stack.values = stack.values[:last]
	return value, true
}

func (stack *Stack) Peek() (int, bool) {
	if len(stack.values) == 0 {
		return 0, false
	}
	return stack.values[len(stack.values)-1], true
}

func (stack *Stack) Len() int {
	return len(stack.values)
}

func (stack *Stack) Empty() bool {
	return len(stack.values) == 0
}
