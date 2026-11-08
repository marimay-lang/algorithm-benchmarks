// Package catalog owns the deterministic application workloads shared by the harness.
package catalog

import "strconv"

type BookState struct{ Tag, Days int }
type Book struct {
	Title  string
	State  BookState
	Serial int
}
type Labelled interface{ Label() string }

func (b *Book) Label() string  { return b.Title }
func stateFor(i int) BookState { return BookState{i % 3, i % 97} }
func stateScore(s BookState) int {
	switch s.Tag {
	case 0:
		return 1
	case 1:
		return s.Days + 2
	case 2:
		return 101
	default:
		panic("state")
	}
}
func titles() []string {
	return []string{"Война и мир", "Мастер и Маргарита", "Ёжик в тумане", "Книга моря", "Белый парус", "Путь домой", "Сад камней", "Зимняя ночь", "The Go Book", "Rust in Action", "Marimay λ", "東京 🚀", "Книга памяти", "Дальний берег", "Тихий Дон", "Алые паруса"}
}
func titleFor(i int, names []string) string { return names[i%len(names)] + " #" + strconv.Itoa(i) }
func books(n int) []*Book {
	names := titles()
	result := []*Book{}
	for i := 0; i < n; i++ {
		result = append(result, &Book{names[i%len(names)], stateFor(i), i})
	}
	return result
}
func add(c, v int) int { return (c + v) % 1_000_000_007 }
func bytesChecksum(s string) int {
	data := []byte(s)
	c := 0
	for i, b := range data {
		c = add(c, (i%251+1)*int(b))
	}
	return c
}
