use marimay_algorithms::graphs::{self, Edge};
use marimay_algorithms::sorting;
use marimay_algorithms::structures::{Dsu, MinHeap, Queue, Stack};

const CHECKSUM_MOD: i64 = 1_000_000_007;

fn generated_values(size: usize, seed: i64) -> Vec<i64> {
    let mut values = Vec::with_capacity(size);
    let mut state = seed;
    for _ in 0..size {
        state = (state * 25_173 + 13_849) % 65_536;
        values.push(state % 20_001 - 10_000);
    }
    values
}

fn add_checksum(checksum: i64, value: i64) -> i64 {
    (checksum + value.rem_euclid(CHECKSUM_MOD)) % CHECKSUM_MOD
}

fn benchmark_insertion() -> i64 {
    let mut checksum = 0;
    for repeat in 0..50 {
        let mut values = generated_values(2_500, repeat + 1);
        sorting::insertion_sort(&mut values);
        checksum = add_checksum(checksum, values[0]);
        checksum = add_checksum(checksum, values[values.len() / 2]);
        checksum = add_checksum(checksum, values[values.len() - 1]);
    }
    checksum
}

fn benchmark_heap_sort() -> i64 {
    let mut checksum = 0;
    for repeat in 0..5 {
        let mut values = generated_values(100_000, repeat + 101);
        sorting::heap_sort(&mut values);
        checksum = add_checksum(checksum, values[0]);
        checksum = add_checksum(checksum, values[values.len() / 2]);
        checksum = add_checksum(checksum, values[values.len() - 1]);
    }
    checksum
}

fn benchmark_stack() -> i64 {
    let mut stack = Stack::new();
    let mut state = 7;
    let mut checksum = 0;
    for _ in 0..1_000_000 {
        state = (state * 25_173 + 13_849) % 65_536;
        stack.push(state % 1_001);
    }
    while let Some(value) = stack.pop() {
        checksum = add_checksum(checksum, value);
    }
    checksum
}

fn benchmark_queue() -> i64 {
    let mut queue = Queue::new();
    let mut state = 11;
    let mut checksum = 0;
    for _ in 0..1_000_000 {
        state = (state * 25_173 + 13_849) % 65_536;
        queue.enqueue(state % 1_001);
    }
    while let Some(value) = queue.dequeue() {
        checksum = add_checksum(checksum, value);
    }
    checksum
}

fn benchmark_min_heap() -> i64 {
    let mut heap = MinHeap::new();
    let mut state = 13;
    let mut checksum = 0;
    for _ in 0..500_000 {
        state = (state * 25_173 + 13_849) % 65_536;
        heap.push(state % 10_001);
    }
    while let Some(value) = heap.pop() {
        checksum = add_checksum(checksum, value);
    }
    checksum
}

fn benchmark_dsu() -> i64 {
    const SIZE: usize = 100_000;
    let mut dsu = Dsu::new(SIZE);
    for operation in 0..5_000_000 {
        let left = operation % SIZE;
        let right = (operation * 17 + 3) % SIZE;
        dsu.union(left, right);
    }
    let mut checksum = dsu.components() as i64;
    for index in (0..SIZE).step_by(97) {
        checksum = add_checksum(checksum, dsu.find(index) as i64);
    }
    checksum
}

fn benchmark_bfs() -> i64 {
    const SIZE: usize = 20_000;
    let adjacency: Vec<Vec<usize>> = (0..SIZE)
        .map(|node| {
            vec![
                (node + 1) % SIZE,
                (node + SIZE - 1) % SIZE,
                (node + 7) % SIZE,
                (node + SIZE - 7) % SIZE,
            ]
        })
        .collect();
    let mut checksum = 0;
    for repeat in 0..300 {
        let distances = graphs::bfs(&adjacency, repeat).expect("valid BFS graph");
        checksum = add_checksum(checksum, distances[(repeat + SIZE / 2) % SIZE]);
        checksum = add_checksum(checksum, distances[(repeat + SIZE / 3) % SIZE]);
    }
    checksum
}

fn benchmark_dijkstra() -> i64 {
    const SIZE: usize = 800;
    let adjacency: Vec<Vec<Edge>> = (0..SIZE)
        .map(|node| {
            let mut edges = Vec::with_capacity(2);
            if node + 1 < SIZE {
                edges.push(Edge {
                    to: node + 1,
                    weight: 1,
                });
            }
            if node + 7 < SIZE {
                edges.push(Edge {
                    to: node + 7,
                    weight: 3,
                });
            }
            edges
        })
        .collect();
    let mut checksum = 0;
    for repeat in 0..80 {
        let distances = graphs::dijkstra(&adjacency, repeat).expect("valid Dijkstra graph");
        checksum = add_checksum(checksum, distances[SIZE - 1]);
        checksum = add_checksum(checksum, distances[SIZE / 2]);
    }
    checksum
}

fn main() {
    let name = std::env::args().nth(1).unwrap_or_else(|| {
        eprintln!("usage: benchmark <insertion|heap-sort|stack|queue|min-heap|dsu|bfs|dijkstra>");
        std::process::exit(2);
    });
    let checksum = match name.as_str() {
        "insertion" => benchmark_insertion(),
        "heap-sort" => benchmark_heap_sort(),
        "stack" => benchmark_stack(),
        "queue" => benchmark_queue(),
        "min-heap" => benchmark_min_heap(),
        "dsu" => benchmark_dsu(),
        "bfs" => benchmark_bfs(),
        "dijkstra" => benchmark_dijkstra(),
        _ => {
            eprintln!("unknown benchmark: {name}");
            std::process::exit(2);
        }
    };
    println!("{name} {checksum}");
}
