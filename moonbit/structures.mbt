///|
pub fn stack_new() -> Array[Int] {
  []
}

///|
pub fn stack_push(stack : Array[Int], value : Int) -> Unit {
  stack.push(value)
}

///|
pub fn stack_pop(stack : Array[Int]) -> Int? {
  stack.pop()
}

///|
pub fn queue_new() -> Array[Int] {
  []
}

///|
pub fn queue_enqueue(queue : Array[Int], value : Int) -> Unit {
  queue.push(value)
}

///|
pub fn queue_dequeue(queue : Array[Int], head : Int) -> Int? {
  if head < queue.length() {
    Some(queue[head])
  } else {
    None
  }
}

///|
pub fn min_heap_new() -> Array[Int] {
  []
}

///|
pub fn min_heap_push(heap : Array[Int], value : Int) -> Unit {
  heap.push(value)
  let mut index = heap.length() - 1
  while index > 0 {
    let parent = (index - 1) / 2
    if heap[parent] <= heap[index] {
      return
    }
    let temporary = heap[parent]
    heap[parent] = heap[index]
    heap[index] = temporary
    index = parent
  }
}

///|
pub fn min_heap_pop(heap : Array[Int]) -> Int? {
  if heap.length() == 0 {
    return None
  }
  let result = heap[0]
  let last = heap.pop().unwrap()
  if heap.length() == 0 {
    return Some(result)
  }
  heap[0] = last
  let mut index = 0
  while true {
    let left = index * 2 + 1
    if left >= heap.length() {
      break
    }
    let right = left + 1
    let mut smallest = left
    if right < heap.length() && heap[right] < heap[left] {
      smallest = right
    }
    if heap[index] <= heap[smallest] {
      break
    }
    let temporary = heap[index]
    heap[index] = heap[smallest]
    heap[smallest] = temporary
    index = smallest
  }
  Some(result)
}

///|
pub fn dsu_new(size : Int) -> (Array[Int], Array[Int]) {
  let parent = Array::make(size, 0)
  for index = 0; index < size; index = index + 1 {
    parent[index] = index
  }
  (parent, Array::make(size, 0))
}

///|
pub fn dsu_find(parent : Array[Int], value : Int) -> Int {
  let mut root = value
  while parent[root] != root {
    root = parent[root]
  }
  let mut current = value
  while parent[current] != current {
    let next = parent[current]
    parent[current] = root
    current = next
  }
  root
}

///|
pub fn dsu_union(
  parent : Array[Int],
  rank : Array[Int],
  left : Int,
  right : Int,
) -> Bool {
  let mut left_root = dsu_find(parent, left)
  let mut right_root = dsu_find(parent, right)
  if left_root == right_root {
    return false
  }
  if rank[left_root] < rank[right_root] {
    let temporary = left_root
    left_root = right_root
    right_root = temporary
  }
  parent[right_root] = left_root
  if rank[left_root] == rank[right_root] {
    rank[left_root] = rank[left_root] + 1
  }
  true
}
