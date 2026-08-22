export function insertionSort(values: number[]): void {
  for (let index = 1; index < values.length; index += 1) {
    const value = values[index];
    let position = index;
    while (position > 0 && values[position - 1] > value) {
      values[position] = values[position - 1];
      position -= 1;
    }
    values[position] = value;
  }
}

function siftDown(values: number[], root: number, size: number): void {
  let current = root;
  while (true) {
    const left = current * 2 + 1;
    if (left >= size) {
      return;
    }
    const right = left + 1;
    let largest = left;
    if (right < size && values[right] > values[left]) {
      largest = right;
    }
    if (values[current] >= values[largest]) {
      return;
    }
    [values[current], values[largest]] = [values[largest], values[current]];
    current = largest;
  }
}

export function heapSort(values: number[]): void {
  for (let root = Math.floor(values.length / 2) - 1; root >= 0; root -= 1) {
    siftDown(values, root, values.length);
  }
  for (let end = values.length - 1; end > 0; end -= 1) {
    [values[0], values[end]] = [values[end], values[0]];
    siftDown(values, 0, end);
  }
}
