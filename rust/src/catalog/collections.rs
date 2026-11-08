use super::*;
use std::collections::{HashMap, HashSet};

pub fn map_int(n: usize, rounds: usize) -> usize {
    let mut counts = HashMap::new();
    for i in 0..n * rounds {
        let key = ((i * 25173 + 13849) % n) as i64;
        let old = *counts.get(&key).unwrap_or(&0);
        counts.insert(key, old + 1);
    }
    let mut c = counts.len();
    for k in 0..n {
        c = add(c, (k + 1) * counts.get(&(k as i64)).unwrap_or(&0));
    }
    c
}
pub fn map_string(n: usize, rounds: usize) -> usize {
    let names = titles();
    let mut keys = Vec::new();
    for i in 0..n {
        keys.push(Rc::<str>::from(title_for(i, &names)));
    }
    let mut counts: HashMap<Rc<str>, usize> = HashMap::new();
    for i in 0..n * rounds {
        let key = &keys[(i * 25173 + 13849) % n];
        let old = *counts.get(key).unwrap_or(&0);
        counts.insert(Rc::clone(key), old + 1);
    }
    let mut c = counts.len();
    for i in 0..n {
        c = add(
            c,
            (i + 1) * counts.get(title_for(i, &names).as_str()).unwrap_or(&0),
        );
    }
    c
}
pub fn map_book(n: usize, rounds: usize) -> usize {
    let names = titles();
    let mut values = HashMap::new();
    for i in 0..n {
        let name = Rc::<str>::from(title_for(i, &names));
        values.insert(
            Rc::clone(&name),
            Rc::new(Book {
                title: name,
                state: state_for(i),
                serial: i,
            }),
        );
    }
    let mut c = 0;
    for _ in 0..rounds {
        for i in 0..n {
            let b = values
                .get(title_for(i, &names).as_str())
                .expect("missing book");
            c = add(c, b.title.len() + state_score(b.state) + b.serial);
        }
    }
    c
}
pub fn set_churn(n: usize, rounds: usize) -> usize {
    let names = titles();
    let mut values = HashSet::new();
    for i in 0..n {
        values.insert(title_for(i, &names));
    }
    let mut c = 0;
    for s in 0..n * rounds {
        assert!(values.remove(&title_for(s, &names)));
        assert!(!values.contains(&title_for(s, &names)));
        values.insert(title_for(s + n, &names));
        c = add(c, values.len());
    }
    for i in n * rounds..n * (rounds + 1) {
        assert!(values.contains(&title_for(i, &names)));
        c = add(c, title_for(i, &names).len());
    }
    c
}
pub fn array_growth(n: usize, rounds: usize, reserved: bool) -> usize {
    let mut c = 0;
    for _ in 0..rounds {
        let mut values = Vec::new();
        if reserved {
            values.reserve(n);
        }
        for i in 0..n {
            values.push((i * 17) % 1009);
        }
        for v in values {
            c = add(c, v);
        }
    }
    c
}
