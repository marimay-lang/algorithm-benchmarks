package catalog

import (
	"strconv"
	"strings"
)

func TitleSearch(n, rounds int) int {
	names := titles()
	values := []string{}
	for i := 0; i < n; i++ {
		values = append(values, titleFor(i, names))
	}
	c := 0
	for q := 0; q < rounds; q++ {
		target := "книги нет"
		if q%4 != 3 {
			target = titleFor(q*7919%n, names)
		}
		found := 0
		for i, v := range values {
			if v == target {
				found = i + 1
				break
			}
		}
		c = add(c, found)
	}
	return c
}

// ownedScalars matches Marimay's owned grapheme pieces for this scalar-only corpus.
func ownedScalars(s string) []string {
	out := []string{}
	for _, r := range s {
		out = append(out, string(r))
	}
	return out
}
func NormalizeTitle(n, rounds int) int {
	upper := ownedScalars("ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
	lower := ownedScalars("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя")
	folding := map[string]string{}
	for i, u := range upper {
		folding[u] = lower[i]
	}
	inputs := []string{" \tВОЙНА И МИР\r\n", "  ЁЖИК В ТУМАНЕ ", " THE GO BOOK\t", " МАСТЕР И МАРГАРИТА "}
	expected := []string{"война и мир", "ёжик в тумане", "the go book", "мастер и маргарита"}
	c := 0
	for r := 0; r < rounds; r++ {
		for i := 0; i < n; i++ {
			var b strings.Builder
			for _, s := range ownedScalars(strings.Trim(inputs[i%4], " \t\n\r\v\f")) {
				f, ok := folding[s]
				if !ok {
					f = s
				}
				b.WriteString(f)
			}
			out := b.String()
			if out != expected[i%4] {
				panic("normalization")
			}
			c = add(c, len(out))
		}
	}
	return c
}
func WordFrequency(n, rounds int) int {
	lines := []string{"книга море книга дом", "море свет дом книга", "rust go marimay go", "ёжик туман ёжик книга"}
	c := 0
	for r := 0; r < rounds; r++ {
		counts := map[string]int{}
		for i := 0; i < n; i++ {
			words := strings.Split(lines[i%4], " ")
			for j, word := range words {
				words[j] = strings.Clone(word)
			}
			for _, w := range words {
				old := counts[w]
				counts[w] = old + 1
			}
		}
		for _, w := range []string{"книга", "море", "дом", "свет", "rust", "go", "marimay", "ёжик", "туман"} {
			c = add(c, counts[w]*len(w))
		}
		c = add(c, len(counts))
	}
	return c
}
func Report(n, rounds int, builderMode bool) int {
	names := titles()
	c := 0
	for r := 0; r < rounds; r++ {
		var b strings.Builder
		result := ""
		for i := 0; i < n; i++ {
			line := strconv.Itoa(i) + "|" + names[i%len(names)] + "|" + strconv.Itoa(i%3) + "\n"
			if builderMode {
				b.WriteString(line)
			} else {
				result = result + line
			}
		}
		if builderMode {
			result = b.String()
		}
		c = add(c, bytesChecksum(result))
	}
	return c
}
