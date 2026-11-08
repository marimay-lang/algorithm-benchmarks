use super::*;
use std::collections::HashMap;

pub fn title_search(n: usize, rounds: usize) -> usize {
    let names = titles();
    let mut values = Vec::new();
    for i in 0..n {
        values.push(title_for(i, &names));
    }
    let mut c = 0;
    for q in 0..rounds {
        let target = if q % 4 != 3 {
            title_for(q * 7919 % n, &names)
        } else {
            "книги нет".into()
        };
        let mut found = 0;
        for (i, v) in values.iter().enumerate() {
            if *v == target {
                found = i + 1;
                break;
            }
        }
        c = add(c, found);
    }
    c
}
fn owned_scalars(s: &str) -> Vec<String> {
    s.chars().map(|r| r.to_string()).collect()
}
pub fn normalize_title(n: usize, rounds: usize) -> usize {
    let upper = owned_scalars("ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ");
    let lower = owned_scalars("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя");
    let mut folding = HashMap::new();
    for (i, u) in upper.into_iter().enumerate() {
        folding.insert(u, lower[i].clone());
    }
    let inputs = [
        " \tВОЙНА И МИР\r\n",
        "  ЁЖИК В ТУМАНЕ ",
        " THE GO BOOK\t",
        " МАСТЕР И МАРГАРИТА ",
    ];
    let expected = [
        "война и мир",
        "ёжик в тумане",
        "the go book",
        "мастер и маргарита",
    ];
    let mut c = 0;
    for _ in 0..rounds {
        for i in 0..n {
            let mut b = String::new();
            for s in
                owned_scalars(inputs[i % 4].trim_matches([' ', '\t', '\n', '\r', '\u{b}', '\u{c}']))
            {
                b.push_str(folding.get(&s).unwrap_or(&s));
            }
            assert_eq!(b, expected[i % 4]);
            c = add(c, b.len());
        }
    }
    c
}
pub fn word_frequency(n: usize, rounds: usize) -> usize {
    let lines = [
        "книга море книга дом",
        "море свет дом книга",
        "rust go marimay go",
        "ёжик туман ёжик книга",
    ];
    let mut c = 0;
    for _ in 0..rounds {
        let mut counts: HashMap<String, usize> = HashMap::new();
        for i in 0..n {
            let words: Vec<String> = lines[i % 4].split(' ').map(str::to_owned).collect();
            for word in words {
                let old = *counts.get(&word).unwrap_or(&0);
                counts.insert(word, old + 1);
            }
        }
        for w in [
            "книга",
            "море",
            "дом",
            "свет",
            "rust",
            "go",
            "marimay",
            "ёжик",
            "туман",
        ] {
            c = add(c, counts.get(w).unwrap_or(&0) * w.len());
        }
        c = add(c, counts.len());
    }
    c
}
pub fn report(n: usize, rounds: usize, builder_mode: bool) -> usize {
    let names = titles();
    let mut c = 0;
    for _ in 0..rounds {
        let mut b = String::new();
        let mut result = String::new();
        for i in 0..n {
            let line = format!("{}|{}|{}\n", i, names[i % names.len()], i % 3);
            if builder_mode {
                b.push_str(&line);
            } else {
                // Explicit fresh immutable concatenation, not Rust's in-place String +.
                result = format!("{result}{line}");
            }
        }
        if builder_mode {
            result = b;
        }
        c = add(c, bytes_checksum(&result));
    }
    c
}
