package catalog

import "strconv"

func interfaceLabel(v Labelled) string { return v.Label() }
func CatalogWalk(n, rounds, mode int) int {
	values := books(n)
	labels := []Labelled{}
	if mode == 2 {
		for _, b := range values {
			labels = append(labels, b)
		}
	}
	c := 0
	for r := 0; r < rounds; r++ {
		for i := 0; i < n; i++ {
			if mode == 0 {
				c = add(c, stateScore(values[i].State)+len(values[i].Title))
			}
			if mode == 1 {
				c = add(c, len(values[i].Label()))
			}
			if mode == 2 {
				c = add(c, len(interfaceLabel(labels[i])))
			}
		}
	}
	return c
}
func RecordCopies(n, rounds int, fresh bool) int {
	original := books(n)
	c := 0
	for r := 0; r < rounds; r++ {
		retained := []*Book{}
		for _, b := range original {
			value := b
			if fresh {
				value = &Book{b.Title, b.State, b.Serial}
			}
			retained = append(retained, value)
		}
		for i, b := range retained {
			identity := 0
			if original[i] == b {
				identity = 1
			}
			c = add(c, b.Serial+len(b.Title)+identity)
		}
	}
	return c
}
func CatalogPipeline(n, rounds int) int {
	values := books(n)
	names := titles()
	c := 0
	for r := 0; r < rounds; r++ {
		counts := map[string]int{}
		for _, b := range values {
			old := counts[b.Title]
			counts[b.Title] = old + 1
			c = add(c, stateScore(b.State))
		}
		for q := 0; q < 64; q++ {
			target := "книги нет"
			if q%4 != 3 {
				target = names[q%len(names)]
			}
			found := 0
			for _, b := range values {
				if b.Title == target {
					found = b.Serial + 1
					break
				}
			}
			c = add(c, found)
			c = add(c, counts[target])
		}
	}
	return c
}
func parsedScore(s string) (int, error) {
	n, err := strconv.Atoi(s)
	if err != nil {
		return 0, err
	}
	return n + 1, nil
}
func ParseResults(n, rounds int) int {
	c := 0
	for r := 0; r < rounds; r++ {
		for i := 0; i < n; i++ {
			token := strconv.Itoa(i % 1009)
			if i%4 == 3 {
				token += "x"
			}
			v, err := parsedScore(token)
			if err != nil {
				v = 7
			}
			c = add(c, v)
		}
	}
	return c
}
