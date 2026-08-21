#[derive(Debug)]
pub struct Dsu {
    parent: Vec<usize>,
    rank: Vec<usize>,
    components: usize,
}

impl Dsu {
    pub fn new(size: usize) -> Self {
        Self {
            parent: (0..size).collect(),
            rank: vec![0; size],
            components: size,
        }
    }

    pub fn find(&mut self, value: usize) -> usize {
        let mut root = value;
        while self.parent[root] != root {
            root = self.parent[root];
        }
        let mut current = value;
        while self.parent[current] != current {
            let next = self.parent[current];
            self.parent[current] = root;
            current = next;
        }
        root
    }

    pub fn union(&mut self, left: usize, right: usize) -> bool {
        let mut left_root = self.find(left);
        let mut right_root = self.find(right);
        if left_root == right_root {
            return false;
        }
        if self.rank[left_root] < self.rank[right_root] {
            std::mem::swap(&mut left_root, &mut right_root);
        }
        self.parent[right_root] = left_root;
        if self.rank[left_root] == self.rank[right_root] {
            self.rank[left_root] += 1;
        }
        self.components -= 1;
        true
    }

    pub fn connected(&mut self, left: usize, right: usize) -> bool {
        self.find(left) == self.find(right)
    }

    pub fn components(&self) -> usize {
        self.components
    }
}
