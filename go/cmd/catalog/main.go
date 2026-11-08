package main

import (
	"example.com/marimay-algorithms/catalog"
	"fmt"
	"os"
	"strconv"
)

func positive(s string) int {
	n, err := strconv.Atoi(s)
	if err != nil || n < 1 || n > 1_000_000 {
		panic("argument outside 1..1000000")
	}
	return n
}
func main() {
	if len(os.Args) != 4 {
		panic("usage: catalog WORKLOAD SIZE ROUNDS")
	}
	name := os.Args[1]
	n := positive(os.Args[2])
	rounds := positive(os.Args[3])
	result := -1
	if name == "title-search-10k" {
		result = catalog.TitleSearch(n, rounds)
	}
	if name == "title-search-100k" {
		result = catalog.TitleSearch(n, rounds)
	}
	if name == "normalize-title" {
		result = catalog.NormalizeTitle(n, rounds)
	}
	if name == "word-frequency" {
		result = catalog.WordFrequency(n, rounds)
	}
	if name == "report-builder" {
		result = catalog.Report(n, rounds, true)
	}
	if name == "report-concat" {
		result = catalog.Report(n, rounds, false)
	}
	if name == "map-int" {
		result = catalog.MapInt(n, rounds)
	}
	if name == "map-string" {
		result = catalog.MapString(n, rounds)
	}
	if name == "map-string-book" {
		result = catalog.MapBook(n, rounds)
	}
	if name == "set-string-churn" {
		result = catalog.SetChurn(n, rounds)
	}
	if name == "catalog-match" {
		result = catalog.CatalogWalk(n, rounds, 0)
	}
	if name == "catalog-dotcall" {
		result = catalog.CatalogWalk(n, rounds, 1)
	}
	if name == "catalog-interface" {
		result = catalog.CatalogWalk(n, rounds, 2)
	}
	if name == "record-reference-copy" {
		result = catalog.RecordCopies(n, rounds, false)
	}
	if name == "record-create" {
		result = catalog.RecordCopies(n, rounds, true)
	}
	if name == "array-grow" {
		result = catalog.ArrayGrowth(n, rounds, false)
	}
	if name == "array-reserved" {
		result = catalog.ArrayGrowth(n, rounds, true)
	}
	if name == "bfs-int" {
		result = catalog.BFS(n, rounds, false)
	}
	if name == "bfs-record" {
		result = catalog.BFS(n, rounds, true)
	}
	if name == "catalog-pipeline" {
		result = catalog.CatalogPipeline(n, rounds)
	}
	if name == "parse-result" {
		result = catalog.ParseResults(n, rounds)
	}
	if result < 0 {
		panic("unknown workload")
	}
	fmt.Printf("%s %d\n", name, result)
}
