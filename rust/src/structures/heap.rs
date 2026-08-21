#[derive(Debug, Default)]
pub struct MinHeap {
    values: Vec<i64>,
}

impl MinHeap {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn push(&mut self, value: i64) {
        self.values.push(value);
        let mut index = self.values.len() - 1;
        while index > 0 {
            let parent = (index - 1) / 2;
            if self.values[parent] <= self.values[index] {
                return;
            }
            self.values.swap(parent, index);
            index = parent;
        }
    }

    pub fn pop(&mut self) -> Option<i64> {
        if self.values.is_empty() {
            return None;
        }
        let minimum = self.values[0];
        let last = self.values.pop().expect("heap was checked as non-empty");
        if !self.values.is_empty() {
            self.values[0] = last;
            self.sift_down(0);
        }
        Some(minimum)
    }

    pub fn peek(&self) -> Option<i64> {
        self.values.first().copied()
    }

    pub fn len(&self) -> usize {
        self.values.len()
    }

    pub fn is_empty(&self) -> bool {
        self.values.is_empty()
    }

    fn sift_down(&mut self, start: usize) {
        let mut index = start;
        while index * 2 + 1 < self.values.len() {
            let left = index * 2 + 1;
            let right = left + 1;
            let mut smallest = left;
            if right < self.values.len() && self.values[right] < self.values[left] {
                smallest = right;
            }
            if self.values[index] <= self.values[smallest] {
                return;
            }
            self.values.swap(index, smallest);
            index = smallest;
        }
    }
}
