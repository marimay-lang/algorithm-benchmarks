use marimay_algorithms::catalog;

#[test]
fn boundary_checksums() {
    assert_eq!(catalog::title_search(1, 3), 3, "title-search-10k/1");
    assert_eq!(catalog::title_search(1, 3), 3, "title-search-100k/1");
    assert_eq!(catalog::normalize_title(1, 3), 60, "normalize-title/1");
    assert_eq!(catalog::word_frequency(1, 3), 111, "word-frequency/1");
    assert_eq!(catalog::report(1, 3, true), 142179, "report-builder/1");
    assert_eq!(catalog::report(1, 3, false), 142179, "report-concat/1");
    assert_eq!(catalog::map_int(1, 3), 4, "map-int/1");
    assert_eq!(catalog::map_string(1, 3), 4, "map-string/1");
    assert_eq!(catalog::map_book(1, 3), 72, "map-string-book/1");
    assert_eq!(catalog::set_churn(1, 3), 25, "set-string-churn/1");
    assert_eq!(catalog::catalog_walk(1, 3, 0), 63, "catalog-match/1");
    assert_eq!(catalog::catalog_walk(1, 3, 1), 60, "catalog-dotcall/1");
    assert_eq!(catalog::catalog_walk(1, 3, 2), 60, "catalog-interface/1");
    assert_eq!(
        catalog::record_copies(1, 3, false),
        63,
        "record-reference-copy/1"
    );
    assert_eq!(catalog::record_copies(1, 3, true), 60, "record-create/1");
    assert_eq!(catalog::array_growth(1, 3, false), 0, "array-grow/1");
    assert_eq!(catalog::array_growth(1, 3, true), 0, "array-reserved/1");
    assert_eq!(catalog::bfs(1, 3, false), 3, "bfs-int/1");
    assert_eq!(catalog::bfs(1, 3, true), 3, "bfs-record/1");
    assert_eq!(catalog::catalog_pipeline(1, 3), 27, "catalog-pipeline/1");
    assert_eq!(catalog::parse_results(1, 3), 3, "parse-result/1");
    assert_eq!(catalog::title_search(17, 3), 28, "title-search-10k/17");
    assert_eq!(catalog::title_search(17, 3), 28, "title-search-100k/17");
    assert_eq!(catalog::normalize_title(17, 3), 1128, "normalize-title/17");
    assert_eq!(catalog::word_frequency(17, 3), 1533, "word-frequency/17");
    assert_eq!(catalog::report(17, 3, true), 19929264, "report-builder/17");
    assert_eq!(catalog::report(17, 3, false), 19929264, "report-concat/17");
    assert_eq!(catalog::map_int(17, 3), 476, "map-int/17");
    assert_eq!(catalog::map_string(17, 3), 476, "map-string/17");
    assert_eq!(catalog::map_book(17, 3), 3291, "map-string-book/17");
    assert_eq!(catalog::set_churn(17, 3), 1263, "set-string-churn/17");
    assert_eq!(catalog::catalog_walk(17, 3, 0), 2709, "catalog-match/17");
    assert_eq!(catalog::catalog_walk(17, 3, 1), 987, "catalog-dotcall/17");
    assert_eq!(catalog::catalog_walk(17, 3, 2), 987, "catalog-interface/17");
    assert_eq!(
        catalog::record_copies(17, 3, false),
        1446,
        "record-reference-copy/17"
    );
    assert_eq!(
        catalog::record_copies(17, 3, true),
        1395,
        "record-create/17"
    );
    assert_eq!(catalog::array_growth(17, 3, false), 6936, "array-grow/17");
    assert_eq!(
        catalog::array_growth(17, 3, true),
        6936,
        "array-reserved/17"
    );
    assert_eq!(catalog::bfs(17, 3, false), 1143, "bfs-int/17");
    assert_eq!(catalog::bfs(17, 3, true), 1143, "bfs-record/17");
    assert_eq!(
        catalog::catalog_pipeline(17, 3),
        3030,
        "catalog-pipeline/17"
    );
    assert_eq!(catalog::parse_results(17, 3), 423, "parse-result/17");
}
