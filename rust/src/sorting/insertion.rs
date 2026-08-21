pub fn insertion_sort(values: &mut [i64]) {
    for index in 1..values.len() {
        let current = values[index];
        let mut position = index;
        while position > 0 && values[position - 1] > current {
            values[position] = values[position - 1];
            position -= 1;
        }
        values[position] = current;
    }
}
