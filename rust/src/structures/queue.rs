#[derive(Debug, Default)]
pub struct Queue {
    values: Vec<i64>,
    head: usize,
}

impl Queue {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn enqueue(&mut self, value: i64) {
        self.values.push(value);
    }

    pub fn dequeue(&mut self) -> Option<i64> {
        let value = self.values.get(self.head).copied()?;
        self.head += 1;
        Some(value)
    }

    pub fn front(&self) -> Option<i64> {
        self.values.get(self.head).copied()
    }

    pub fn len(&self) -> usize {
        self.values.len() - self.head
    }

    pub fn is_empty(&self) -> bool {
        self.head == self.values.len()
    }
}
