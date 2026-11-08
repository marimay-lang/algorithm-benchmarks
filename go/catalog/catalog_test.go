package catalog

import "testing"

// Independent reference checks for singleton and uneven corpus cycles.
func TestBoundaryChecksums(t *testing.T) {
	if got := TitleSearch(1, 3); got != 3 {
		t.Errorf("title-search-10k/1: got %d, want 3", got)
	}
	if got := TitleSearch(1, 3); got != 3 {
		t.Errorf("title-search-100k/1: got %d, want 3", got)
	}
	if got := NormalizeTitle(1, 3); got != 60 {
		t.Errorf("normalize-title/1: got %d, want 60", got)
	}
	if got := WordFrequency(1, 3); got != 111 {
		t.Errorf("word-frequency/1: got %d, want 111", got)
	}
	if got := Report(1, 3, true); got != 142179 {
		t.Errorf("report-builder/1: got %d, want 142179", got)
	}
	if got := Report(1, 3, false); got != 142179 {
		t.Errorf("report-concat/1: got %d, want 142179", got)
	}
	if got := MapInt(1, 3); got != 4 {
		t.Errorf("map-int/1: got %d, want 4", got)
	}
	if got := MapString(1, 3); got != 4 {
		t.Errorf("map-string/1: got %d, want 4", got)
	}
	if got := MapBook(1, 3); got != 72 {
		t.Errorf("map-string-book/1: got %d, want 72", got)
	}
	if got := SetChurn(1, 3); got != 25 {
		t.Errorf("set-string-churn/1: got %d, want 25", got)
	}
	if got := CatalogWalk(1, 3, 0); got != 63 {
		t.Errorf("catalog-match/1: got %d, want 63", got)
	}
	if got := CatalogWalk(1, 3, 1); got != 60 {
		t.Errorf("catalog-dotcall/1: got %d, want 60", got)
	}
	if got := CatalogWalk(1, 3, 2); got != 60 {
		t.Errorf("catalog-interface/1: got %d, want 60", got)
	}
	if got := RecordCopies(1, 3, false); got != 63 {
		t.Errorf("record-reference-copy/1: got %d, want 63", got)
	}
	if got := RecordCopies(1, 3, true); got != 60 {
		t.Errorf("record-create/1: got %d, want 60", got)
	}
	if got := ArrayGrowth(1, 3, false); got != 0 {
		t.Errorf("array-grow/1: got %d, want 0", got)
	}
	if got := ArrayGrowth(1, 3, true); got != 0 {
		t.Errorf("array-reserved/1: got %d, want 0", got)
	}
	if got := BFS(1, 3, false); got != 3 {
		t.Errorf("bfs-int/1: got %d, want 3", got)
	}
	if got := BFS(1, 3, true); got != 3 {
		t.Errorf("bfs-record/1: got %d, want 3", got)
	}
	if got := CatalogPipeline(1, 3); got != 27 {
		t.Errorf("catalog-pipeline/1: got %d, want 27", got)
	}
	if got := ParseResults(1, 3); got != 3 {
		t.Errorf("parse-result/1: got %d, want 3", got)
	}
	if got := TitleSearch(17, 3); got != 28 {
		t.Errorf("title-search-10k/17: got %d, want 28", got)
	}
	if got := TitleSearch(17, 3); got != 28 {
		t.Errorf("title-search-100k/17: got %d, want 28", got)
	}
	if got := NormalizeTitle(17, 3); got != 1128 {
		t.Errorf("normalize-title/17: got %d, want 1128", got)
	}
	if got := WordFrequency(17, 3); got != 1533 {
		t.Errorf("word-frequency/17: got %d, want 1533", got)
	}
	if got := Report(17, 3, true); got != 19929264 {
		t.Errorf("report-builder/17: got %d, want 19929264", got)
	}
	if got := Report(17, 3, false); got != 19929264 {
		t.Errorf("report-concat/17: got %d, want 19929264", got)
	}
	if got := MapInt(17, 3); got != 476 {
		t.Errorf("map-int/17: got %d, want 476", got)
	}
	if got := MapString(17, 3); got != 476 {
		t.Errorf("map-string/17: got %d, want 476", got)
	}
	if got := MapBook(17, 3); got != 3291 {
		t.Errorf("map-string-book/17: got %d, want 3291", got)
	}
	if got := SetChurn(17, 3); got != 1263 {
		t.Errorf("set-string-churn/17: got %d, want 1263", got)
	}
	if got := CatalogWalk(17, 3, 0); got != 2709 {
		t.Errorf("catalog-match/17: got %d, want 2709", got)
	}
	if got := CatalogWalk(17, 3, 1); got != 987 {
		t.Errorf("catalog-dotcall/17: got %d, want 987", got)
	}
	if got := CatalogWalk(17, 3, 2); got != 987 {
		t.Errorf("catalog-interface/17: got %d, want 987", got)
	}
	if got := RecordCopies(17, 3, false); got != 1446 {
		t.Errorf("record-reference-copy/17: got %d, want 1446", got)
	}
	if got := RecordCopies(17, 3, true); got != 1395 {
		t.Errorf("record-create/17: got %d, want 1395", got)
	}
	if got := ArrayGrowth(17, 3, false); got != 6936 {
		t.Errorf("array-grow/17: got %d, want 6936", got)
	}
	if got := ArrayGrowth(17, 3, true); got != 6936 {
		t.Errorf("array-reserved/17: got %d, want 6936", got)
	}
	if got := BFS(17, 3, false); got != 1143 {
		t.Errorf("bfs-int/17: got %d, want 1143", got)
	}
	if got := BFS(17, 3, true); got != 1143 {
		t.Errorf("bfs-record/17: got %d, want 1143", got)
	}
	if got := CatalogPipeline(17, 3); got != 3030 {
		t.Errorf("catalog-pipeline/17: got %d, want 3030", got)
	}
	if got := ParseResults(17, 3); got != 423 {
		t.Errorf("parse-result/17: got %d, want 423", got)
	}
}
