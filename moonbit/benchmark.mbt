///|
let checksum_mod = 1_000_000_007

///|
fn generated_values(size : Int, seed : Int) -> Array[Int] {
  let values = Array::make(size, 0)
  let mut state = seed
  for index = 0; index < size; index = index + 1 {
    state = (state * 25_173 + 13_849) % 65_536
    values[index] = state % 20_001 - 10_000
  }
  values
}

///|
fn add_checksum(checksum : Int, source_value : Int) -> Int {
  let mut value = source_value % checksum_mod
  if value < 0 {
    value = value + checksum_mod
  }
  (checksum + value) % checksum_mod
}

///|
fn benchmark_insertion() -> Int {
  let mut checksum = 0
  for repeat = 0; repeat < 50; repeat = repeat + 1 {
    let values = generated_values(2_500, repeat + 1)
    insertion_sort(values)
    checksum = add_checksum(checksum, values[0])
    checksum = add_checksum(checksum, values[values.length() / 2])
    checksum = add_checksum(checksum, values[values.length() - 1])
  }
  checksum
}

///|
fn benchmark_heap_sort() -> Int {
  let mut checksum = 0
  for repeat = 0; repeat < 5; repeat = repeat + 1 {
    let values = generated_values(100_000, repeat + 101)
    heap_sort(values)
    checksum = add_checksum(checksum, values[0])
    checksum = add_checksum(checksum, values[values.length() / 2])
    checksum = add_checksum(checksum, values[values.length() - 1])
  }
  checksum
}

///|
fn benchmark_stack() -> Int {
  let stack = stack_new()
  let mut state = 7
  let mut checksum = 0
  for index = 0; index < 1_000_000; index = index + 1 {
    state = (state * 25_173 + 13_849) % 65_536
    stack_push(stack, state % 1_001)
  }
  while stack.length() > 0 {
    checksum = add_checksum(checksum, stack_pop(stack).unwrap())
  }
  checksum
}

///|
fn benchmark_queue() -> Int {
  let queue = queue_new()
  let mut state = 11
  let mut checksum = 0
  for index = 0; index < 1_000_000; index = index + 1 {
    state = (state * 25_173 + 13_849) % 65_536
    queue_enqueue(queue, state % 1_001)
  }
  for head = 0; head < queue.length(); head = head + 1 {
    checksum = add_checksum(checksum, queue_dequeue(queue, head).unwrap())
  }
  checksum
}

///|
fn benchmark_min_heap() -> Int {
  let heap = min_heap_new()
  let mut state = 13
  let mut checksum = 0
  for index = 0; index < 500_000; index = index + 1 {
    state = (state * 25_173 + 13_849) % 65_536
    min_heap_push(heap, state % 10_001)
  }
  while heap.length() > 0 {
    checksum = add_checksum(checksum, min_heap_pop(heap).unwrap())
  }
  checksum
}

///|
fn benchmark_dsu() -> Int {
  let size = 100_000
  let (parent, rank) = dsu_new(size)
  let mut components = size
  for operation = 0; operation < 5_000_000; operation = operation + 1 {
    if dsu_union(parent, rank, operation % size, (operation * 17 + 3) % size) {
      components = components - 1
    }
  }
  let mut checksum = components
  for index = 0; index < size; index = index + 97 {
    checksum = add_checksum(checksum, dsu_find(parent, index))
  }
  checksum
}

///|
fn benchmark_bfs() -> Int {
  let size = 20_000
  let adjacency = Array::makei(size, fn(node) {
    [
      (node + 1) % size,
      (node + size - 1) % size,
      (node + 7) % size,
      (node + size - 7) % size,
    ]
  })
  let mut checksum = 0
  for repeat = 0; repeat < 300; repeat = repeat + 1 {
    let distances = bfs(adjacency, repeat).unwrap()
    checksum = add_checksum(checksum, distances[(repeat + size / 2) % size])
    checksum = add_checksum(checksum, distances[(repeat + size / 3) % size])
  }
  checksum
}

///|
fn benchmark_dijkstra() -> Int {
  let size = 800
  let adjacency = Array::makei(size, fn(node) {
    let edges : Array[Edge] = []
    if node + 1 < size {
      edges.push({ to: node + 1, weight: 1 })
    }
    if node + 7 < size {
      edges.push({ to: node + 7, weight: 3 })
    }
    edges
  })
  let mut checksum = 0
  for repeat = 0; repeat < 80; repeat = repeat + 1 {
    let distances = dijkstra(adjacency, repeat).unwrap()
    checksum = add_checksum(checksum, distances[size - 1])
    checksum = add_checksum(checksum, distances[size / 2])
  }
  checksum
}

///|
pub fn run(name : String) -> Int? {
  match name {
    "insertion" => Some(benchmark_insertion())
    "heap-sort" => Some(benchmark_heap_sort())
    "stack" => Some(benchmark_stack())
    "queue" => Some(benchmark_queue())
    "min-heap" => Some(benchmark_min_heap())
    "dsu" => Some(benchmark_dsu())
    "bfs" => Some(benchmark_bfs())
    "dijkstra" => Some(benchmark_dijkstra())
    _ => None
  }
}
