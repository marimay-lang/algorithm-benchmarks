use super::*;
use std::collections::HashMap;
fn interface_label(value: &dyn Labelled) -> &str {
    value.label()
}
pub fn catalog_walk(n: usize, rounds: usize, mode: usize) -> usize {
    let values = books(n);
    let mut labels: Vec<Rc<dyn Labelled>> = Vec::new();
    if mode == 2 {
        for b in &values {
            labels.push(b.clone());
        }
    }
    let mut c = 0;
    for _ in 0..rounds {
        for i in 0..n {
            if mode == 0 {
                c = add(c, state_score(values[i].state) + values[i].title.len());
            }
            if mode == 1 {
                c = add(c, values[i].label().len());
            }
            if mode == 2 {
                c = add(c, interface_label(labels[i].as_ref()).len());
            }
        }
    }
    c
}
pub fn record_copies(n: usize, rounds: usize, fresh: bool) -> usize {
    let original = books(n);
    let mut c = 0;
    for _ in 0..rounds {
        let mut retained = Vec::new();
        for b in &original {
            let value = if fresh {
                Rc::new(Book {
                    title: Rc::clone(&b.title),
                    state: b.state,
                    serial: b.serial,
                })
            } else {
                Rc::clone(b)
            };
            retained.push(value);
        }
        for (i, b) in retained.iter().enumerate() {
            let identity = usize::from(Rc::ptr_eq(&original[i], b));
            c = add(c, b.serial + b.title.len() + identity);
        }
    }
    c
}
pub fn catalog_pipeline(n: usize, rounds: usize) -> usize {
    let values = books(n);
    let names = titles();
    let mut c = 0;
    for _ in 0..rounds {
        let mut counts: HashMap<Rc<str>, usize> = HashMap::new();
        for b in &values {
            let old = *counts.get(&b.title).unwrap_or(&0);
            counts.insert(Rc::clone(&b.title), old + 1);
            c = add(c, state_score(b.state));
        }
        for q in 0..64 {
            let target = if q % 4 != 3 {
                &names[q % names.len()]
            } else {
                "книги нет"
            };
            let mut found = 0;
            for b in &values {
                if b.title.as_ref() == target {
                    found = b.serial + 1;
                    break;
                }
            }
            c = add(c, found);
            c = add(c, *counts.get(target).unwrap_or(&0));
        }
    }
    c
}
fn parsed_score(s: &str) -> Result<usize, std::num::ParseIntError> {
    let n = s.parse::<usize>()?;
    Ok(n + 1)
}
pub fn parse_results(n: usize, rounds: usize) -> usize {
    let mut c = 0;
    for _ in 0..rounds {
        for i in 0..n {
            let mut token = (i % 1009).to_string();
            if i % 4 == 3 {
                token = format!("{token}x");
            }
            c = add(c, parsed_score(&token).unwrap_or(7));
        }
    }
    c
}
