fn sift_down(values: &mut [i64], start: usize, size: usize) {
    let mut root = start;
    while root * 2 + 1 < size {
        let left = root * 2 + 1;
        let right = left + 1;
        let mut largest = left;
        if right < size && values[right] > values[left] {
            largest = right;
        }
        if values[root] >= values[largest] {
            return;
        }
        values.swap(root, largest);
        root = largest;
    }
}

pub fn heap_sort(values: &mut [i64]) {
    let size = values.len();
    if size < 2 {
        return;
    }
    for root in (0..size / 2).rev() {
        sift_down(values, root, size);
    }
    for end in (1..size).rev() {
        values.swap(0, end);
        sift_down(values, 0, end);
    }
}
