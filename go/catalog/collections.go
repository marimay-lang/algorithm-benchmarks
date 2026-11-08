package catalog

func MapInt(n, rounds int) int {
	counts := map[int]int{}
	for i := 0; i < n*rounds; i++ {
		k := (i*25173 + 13849) % n
		old := counts[k]
		counts[k] = old + 1
	}
	c := len(counts)
	for k := 0; k < n; k++ {
		c = add(c, (k+1)*counts[k])
	}
	return c
}
func MapString(n, rounds int) int {
	names := titles()
	keys := []string{}
	for i := 0; i < n; i++ {
		keys = append(keys, titleFor(i, names))
	}
	counts := map[string]int{}
	for i := 0; i < n*rounds; i++ {
		k := keys[(i*25173+13849)%n]
		old := counts[k]
		counts[k] = old + 1
	}
	c := len(counts)
	for i := 0; i < n; i++ {
		c = add(c, (i+1)*counts[titleFor(i, names)])
	}
	return c
}
func MapBook(n, rounds int) int {
	names := titles()
	values := map[string]*Book{}
	for i := 0; i < n; i++ {
		name := titleFor(i, names)
		values[name] = &Book{name, stateFor(i), i}
	}
	c := 0
	for r := 0; r < rounds; r++ {
		for i := 0; i < n; i++ {
			b, ok := values[titleFor(i, names)]
			if !ok {
				panic("missing book")
			}
			c = add(c, len(b.Title)+stateScore(b.State)+b.Serial)
		}
	}
	return c
}
func SetChurn(n, rounds int) int {
	names := titles()
	values := map[string]struct{}{}
	for i := 0; i < n; i++ {
		values[titleFor(i, names)] = struct{}{}
	}
	c := 0
	for s := 0; s < n*rounds; s++ {
		key := titleFor(s, names)
		previousSize := len(values)
		delete(values, key)
		if len(values) != previousSize-1 {
			panic("missing removal")
		}
		if _, ok := values[titleFor(s, names)]; ok {
			panic("removed key")
		}
		values[titleFor(s+n, names)] = struct{}{}
		c = add(c, len(values))
	}
	for i := n * rounds; i < n*(rounds+1); i++ {
		if _, ok := values[titleFor(i, names)]; !ok {
			panic("missing final")
		}
		c = add(c, len(titleFor(i, names)))
	}
	return c
}
func ArrayGrowth(n, rounds int, reserved bool) int {
	c := 0
	for r := 0; r < rounds; r++ {
		values := []int{}
		if reserved {
			values = make([]int, 0, n)
		}
		for i := 0; i < n; i++ {
			values = append(values, i*17%1009)
		}
		for _, v := range values {
			c = add(c, v)
		}
	}
	return c
}
