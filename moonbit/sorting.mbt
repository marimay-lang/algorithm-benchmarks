///|
pub fn insertion_sort(values : Array[Int]) -> Unit {
  for index = 1; index < values.length(); index = index + 1 {
    let value = values[index]
    let mut position = index
    while position > 0 && values[position - 1] > value {
      values[position] = values[position - 1]
      position = position - 1
    }
    values[position] = value
  }
}

///|
fn sift_down(values : Array[Int], root : Int, size : Int) -> Unit {
  let mut current = root
  while true {
    let left = current * 2 + 1
    if left >= size {
      return
    }
    let right = left + 1
    let mut largest = left
    if right < size && values[right] > values[left] {
      largest = right
    }
    if values[current] >= values[largest] {
      return
    }
    let temporary = values[current]
    values[current] = values[largest]
    values[largest] = temporary
    current = largest
  }
}

///|
pub fn heap_sort(values : Array[Int]) -> Unit {
  for root = values.length() / 2 - 1; root >= 0; root = root - 1 {
    sift_down(values, root, values.length())
  }
  for end = values.length() - 1; end > 0; end = end - 1 {
    let temporary = values[0]
    values[0] = values[end]
    values[end] = temporary
    sift_down(values, 0, end)
  }
}
