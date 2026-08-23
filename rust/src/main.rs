use marimay_algorithms::graphs;
use marimay_algorithms::sorting;
use marimay_algorithms::structures::MinHeap;

fn main() {
    let mut values = vec![5, 1, 4, 2, 3];
    sorting::heap_sort(&mut values);
    let mut heap = MinHeap::new();
    heap.push(3);
    heap.push(1);
    let distances = graphs::bfs(&[vec![1], vec![0, 2], vec![1]], 0);
    assert_eq!(values, [1, 2, 3, 4, 5]);
    assert_eq!(heap.pop(), Some(1));
    assert_eq!(distances, Some(vec![0, 1, 2]));
    println!("Rust algorithms: ok");
}
