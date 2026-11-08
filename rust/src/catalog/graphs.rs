use super::*;
struct Node {
    id: usize,
    neighbors: Rc<Vec<usize>>,
}
pub fn bfs(n: usize, rounds: usize, records: bool) -> usize {
    let mut graph = Vec::new();
    let mut nodes = Vec::new();
    for i in 0..n {
        let mut edges = Vec::new();
        for e in 1..17 {
            edges.push((i + e * e) % n);
        }
        let edges = Rc::new(edges);
        graph.push(Rc::clone(&edges));
        if records {
            nodes.push(Rc::new(Node {
                id: i,
                neighbors: edges,
            }));
        }
    }
    let mut c = 0;
    for _ in 0..rounds {
        let mut distances = Vec::new();
        for _ in 0..n {
            distances.push(-1_i64);
        }
        distances[0] = 0;
        let mut queue = Vec::new();
        let mut objects = Vec::new();
        if records {
            objects.push(Rc::clone(&nodes[0]));
        } else {
            queue.push(0);
        }
        for head in 0..n {
            let (index, edges) = if records {
                (objects[head].id, Rc::clone(&objects[head].neighbors))
            } else {
                (queue[head], Rc::clone(&graph[queue[head]]))
            };
            for &neighbor in edges.iter() {
                if distances[neighbor] == -1 {
                    distances[neighbor] = distances[index] + 1;
                    if records {
                        objects.push(Rc::clone(&nodes[neighbor]));
                    } else {
                        queue.push(neighbor);
                    }
                }
            }
        }
        for (i, d) in distances.iter().enumerate() {
            c = add(c, (i + 1) * (d + 1) as usize);
        }
    }
    c
}
