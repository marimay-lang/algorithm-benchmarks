//! Deterministic catalogue workloads. Rc models observable reference identity.
use std::rc::Rc;
mod collections;
mod graphs;
mod objects;
mod text;
pub use collections::*;
pub use graphs::*;
pub use objects::*;
pub use text::*;

#[derive(Clone, Copy)]
enum BookState {
    Available,
    Loaned(usize),
    Missing,
}
struct Book {
    title: Rc<str>,
    state: BookState,
    serial: usize,
}
trait Labelled {
    fn label(&self) -> &str;
}
impl Labelled for Book {
    fn label(&self) -> &str {
        &self.title
    }
}
fn state_for(i: usize) -> BookState {
    match i % 3 {
        0 => BookState::Available,
        1 => BookState::Loaned(i % 97),
        _ => BookState::Missing,
    }
}
fn state_score(s: BookState) -> usize {
    match s {
        BookState::Available => 1,
        BookState::Loaned(d) => d + 2,
        BookState::Missing => 101,
    }
}
fn titles() -> Vec<Rc<str>> {
    [
        "Война и мир",
        "Мастер и Маргарита",
        "Ёжик в тумане",
        "Книга моря",
        "Белый парус",
        "Путь домой",
        "Сад камней",
        "Зимняя ночь",
        "The Go Book",
        "Rust in Action",
        "Marimay λ",
        "東京 🚀",
        "Книга памяти",
        "Дальний берег",
        "Тихий Дон",
        "Алые паруса",
    ]
    .iter()
    .map(|s| Rc::from(*s))
    .collect()
}
fn title_for(i: usize, names: &[Rc<str>]) -> String {
    format!("{} #{}", names[i % names.len()], i)
}
fn books(n: usize) -> Vec<Rc<Book>> {
    let names = titles();
    let mut out = Vec::new();
    for i in 0..n {
        out.push(Rc::new(Book {
            title: Rc::clone(&names[i % names.len()]),
            state: state_for(i),
            serial: i,
        }));
    }
    out
}
fn add(c: usize, v: usize) -> usize {
    (c + v) % 1_000_000_007
}
fn bytes_checksum(s: &str) -> usize {
    let data = s.as_bytes().to_vec();
    let mut c = 0;
    for (i, b) in data.iter().enumerate() {
        c = add(c, (i % 251 + 1) * usize::from(*b));
    }
    c
}
