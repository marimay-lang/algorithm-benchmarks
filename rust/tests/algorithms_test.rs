use marimay_algorithms::counting;
use marimay_algorithms::graphs::{self, Edge};
use marimay_algorithms::sorting;
use marimay_algorithms::structures::{Dsu, MinHeap, Queue, Stack};

#[test]
fn sorting_algorithms() {
    let mut insertion_values = vec![5, -1, 5, 3, 0];
    sorting::insertion_sort(&mut insertion_values);
    assert_eq!(insertion_values, [-1, 0, 3, 5, 5]);
    let mut heap_values = vec![9, 4, 7, 1, -2, 6, 5];
    sorting::heap_sort(&mut heap_values);
    assert_eq!(heap_values, [-2, 1, 4, 5, 6, 7, 9]);
}

#[test]
fn data_structures() {
    let mut stack = Stack::new();
    stack.push(10);
    stack.push(20);
    stack.push(30);
    assert_eq!(stack.pop(), Some(30));
    let mut queue = Queue::new();
    queue.enqueue(10);
    queue.enqueue(20);
    queue.enqueue(30);
    assert_eq!(queue.dequeue(), Some(10));
    let mut heap = MinHeap::new();
    for value in [7, 2, 9, 1, 5] {
        heap.push(value);
    }
    assert_eq!(heap.pop(), Some(1));
    let mut dsu = Dsu::new(6);
    dsu.union(0, 1);
    dsu.union(1, 2);
    dsu.union(3, 4);
    assert!(dsu.connected(0, 2));
    assert!(!dsu.connected(0, 3));
    assert_eq!(dsu.components(), 3);
}

#[test]
fn graph_algorithms() {
    let unweighted = vec![
        vec![1, 2],
        vec![0, 3],
        vec![0, 3, 4],
        vec![1, 2, 4],
        vec![2, 3],
    ];
    assert_eq!(graphs::bfs(&unweighted, 0), Some(vec![0, 1, 1, 2, 2]));
    let weighted = vec![
        vec![Edge { to: 1, weight: 4 }, Edge { to: 2, weight: 1 }],
        vec![Edge { to: 3, weight: 1 }],
        vec![Edge { to: 1, weight: 2 }, Edge { to: 3, weight: 5 }],
        vec![Edge { to: 4, weight: 3 }],
        vec![],
    ];
    assert_eq!(graphs::dijkstra(&weighted, 0), Some(vec![0, 3, 1, 4, 7]));
}

#[test]
fn invalid_graph_inputs() {
    assert_eq!(graphs::bfs(&[], 1), None);
    assert_eq!(graphs::bfs(&[vec![1], vec![2]], 0), None);
    assert_eq!(graphs::dijkstra(&[], 1), None);
    assert_eq!(
        graphs::dijkstra(&[vec![Edge { to: 2, weight: 1 }], vec![]], 0,),
        None,
    );
    assert_eq!(
        graphs::dijkstra(&[vec![Edge { to: 1, weight: -1 }], vec![]], 0,),
        None,
    );
}

#[test]
fn counting_algorithms() {
    let values = [2, 1, 2, -4, 1, 2];
    let counts = counting::int_frequencies(&values);
    assert_eq!(counts.len(), 3);
    assert_eq!(counts.get(&2), Some(&3));
    assert_eq!(counts.get(&99), None);
    assert_eq!(counting::unique_int_count(&values), 3);
    let characters: Vec<char> = "λλ🚀".chars().collect();
    let rune_counts = counting::rune_frequencies(&characters);
    assert_eq!(rune_counts.len(), 2);
    assert_eq!(rune_counts.get(&'λ'), Some(&2));
    assert_eq!(rune_counts.get(&'🚀'), Some(&1));
}
