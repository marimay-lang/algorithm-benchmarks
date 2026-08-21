#[derive(Debug, Default)]
pub struct Stack {
    values: Vec<i64>,
}

impl Stack {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn push(&mut self, value: i64) {
        self.values.push(value);
    }

    pub fn pop(&mut self) -> Option<i64> {
        self.values.pop()
    }

    pub fn peek(&self) -> Option<i64> {
        self.values.last().copied()
    }

    pub fn len(&self) -> usize {
        self.values.len()
    }

    pub fn is_empty(&self) -> bool {
        self.values.is_empty()
    }
}
