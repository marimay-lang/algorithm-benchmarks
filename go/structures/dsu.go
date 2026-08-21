package structures

type DSU struct {
	parent     []int
	rank       []int
	components int
}

func NewDSU(size int) *DSU {
	parent := make([]int, size)
	for index := range parent {
		parent[index] = index
	}
	return &DSU{parent: parent, rank: make([]int, size), components: size}
}

func (dsu *DSU) Find(value int) int {
	root := value
	for dsu.parent[root] != root {
		root = dsu.parent[root]
	}
	for dsu.parent[value] != value {
		next := dsu.parent[value]
		dsu.parent[value] = root
		value = next
	}
	return root
}

func (dsu *DSU) Union(left, right int) bool {
	leftRoot := dsu.Find(left)
	rightRoot := dsu.Find(right)
	if leftRoot == rightRoot {
		return false
	}
	if dsu.rank[leftRoot] < dsu.rank[rightRoot] {
		leftRoot, rightRoot = rightRoot, leftRoot
	}
	dsu.parent[rightRoot] = leftRoot
	if dsu.rank[leftRoot] == dsu.rank[rightRoot] {
		dsu.rank[leftRoot]++
	}
	dsu.components--
	return true
}

func (dsu *DSU) Connected(left, right int) bool {
	return dsu.Find(left) == dsu.Find(right)
}

func (dsu *DSU) Components() int {
	return dsu.components
}
