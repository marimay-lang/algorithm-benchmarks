// Package counting provides reusable frequency and distinct-value algorithms.
package counting

// IntFrequencies counts each integer in values.
func IntFrequencies(values []int) map[int]int {
	counts := make(map[int]int)
	for _, value := range values {
		counts[value]++
	}
	return counts
}

// UniqueIntCount returns the number of distinct integers in values.
func UniqueIntCount(values []int) int {
	unique := make(map[int]struct{})
	for _, value := range values {
		unique[value] = struct{}{}
	}
	return len(unique)
}

// RuneFrequencies counts each Unicode code point in values.
func RuneFrequencies(values []rune) map[rune]int {
	counts := make(map[rune]int)
	for _, value := range values {
		counts[value]++
	}
	return counts
}
