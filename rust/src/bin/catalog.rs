use marimay_algorithms::catalog;
fn positive(s: &str) -> usize {
    let n = s.parse::<usize>().expect("invalid integer");
    assert!((1..=1_000_000).contains(&n));
    n
}
fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    assert_eq!(args.len(), 3, "usage: catalog WORKLOAD SIZE ROUNDS");
    let name = &args[0];
    let n = positive(&args[1]);
    let rounds = positive(&args[2]);
    let result = match name.as_str() {
        "title-search-10k" => catalog::title_search(n, rounds),
        "title-search-100k" => catalog::title_search(n, rounds),
        "normalize-title" => catalog::normalize_title(n, rounds),
        "word-frequency" => catalog::word_frequency(n, rounds),
        "report-builder" => catalog::report(n, rounds, true),
        "report-concat" => catalog::report(n, rounds, false),
        "map-int" => catalog::map_int(n, rounds),
        "map-string" => catalog::map_string(n, rounds),
        "map-string-book" => catalog::map_book(n, rounds),
        "set-string-churn" => catalog::set_churn(n, rounds),
        "catalog-match" => catalog::catalog_walk(n, rounds, 0),
        "catalog-dotcall" => catalog::catalog_walk(n, rounds, 1),
        "catalog-interface" => catalog::catalog_walk(n, rounds, 2),
        "record-reference-copy" => catalog::record_copies(n, rounds, false),
        "record-create" => catalog::record_copies(n, rounds, true),
        "array-grow" => catalog::array_growth(n, rounds, false),
        "array-reserved" => catalog::array_growth(n, rounds, true),
        "bfs-int" => catalog::bfs(n, rounds, false),
        "bfs-record" => catalog::bfs(n, rounds, true),
        "catalog-pipeline" => catalog::catalog_pipeline(n, rounds),
        "parse-result" => catalog::parse_results(n, rounds),
        _ => panic!("unknown workload"),
    };
    println!("{name} {result}");
}
