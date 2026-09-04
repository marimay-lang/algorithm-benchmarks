use std::collections::{HashMap, HashSet};

pub fn int_frequencies(values: &[i64]) -> HashMap<i64, i64> {
    let mut counts = HashMap::new();
    for &value in values {
        *counts.entry(value).or_insert(0) += 1;
    }
    counts
}

pub fn unique_int_count(values: &[i64]) -> usize {
    values.iter().copied().collect::<HashSet<_>>().len()
}

pub fn rune_frequencies(values: &[char]) -> HashMap<char, i64> {
    let mut counts = HashMap::new();
    for &value in values {
        *counts.entry(value).or_insert(0) += 1;
    }
    counts
}
