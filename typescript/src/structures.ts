export class Stack {
  private readonly values: number[] = [];

  push(value: number): void {
    this.values.push(value);
  }

  pop(): number | undefined {
    return this.values.pop();
  }

  empty(): boolean {
    return this.values.length === 0;
  }
}

export class Queue {
  private readonly values: number[] = [];
  private head = 0;

  enqueue(value: number): void {
    this.values.push(value);
  }

  dequeue(): number | undefined {
    if (this.head >= this.values.length) {
      return undefined;
    }
    const value = this.values[this.head];
    this.head += 1;
    return value;
  }

  empty(): boolean {
    return this.head >= this.values.length;
  }
}

export class MinHeap {
  private readonly values: number[] = [];

  push(value: number): void {
    let index = this.values.length;
    this.values.push(value);
    while (index > 0) {
      const parent = Math.floor((index - 1) / 2);
      if (this.values[parent] <= this.values[index]) {
        return;
      }
      [this.values[parent], this.values[index]] = [
        this.values[index],
        this.values[parent],
      ];
      index = parent;
    }
  }

  pop(): number | undefined {
    if (this.values.length === 0) {
      return undefined;
    }
    const result = this.values[0];
    const last = this.values.pop() as number;
    if (this.values.length === 0) {
      return result;
    }
    this.values[0] = last;
    let index = 0;
    while (true) {
      const left = index * 2 + 1;
      if (left >= this.values.length) {
        break;
      }
      const right = left + 1;
      let smallest = left;
      if (right < this.values.length && this.values[right] < this.values[left]) {
        smallest = right;
      }
      if (this.values[index] <= this.values[smallest]) {
        break;
      }
      [this.values[index], this.values[smallest]] = [
        this.values[smallest],
        this.values[index],
      ];
      index = smallest;
    }
    return result;
  }

  empty(): boolean {
    return this.values.length === 0;
  }
}

export class Dsu {
  private readonly parent: number[];
  private readonly rank: number[];
  private componentCount: number;

  constructor(size: number) {
    this.parent = Array.from({ length: size }, (_, index) => index);
    this.rank = new Array<number>(size).fill(0);
    this.componentCount = size;
  }

  find(value: number): number {
    let root = value;
    while (this.parent[root] !== root) {
      root = this.parent[root];
    }
    let current = value;
    while (this.parent[current] !== current) {
      const next = this.parent[current];
      this.parent[current] = root;
      current = next;
    }
    return root;
  }

  union(left: number, right: number): void {
    let leftRoot = this.find(left);
    let rightRoot = this.find(right);
    if (leftRoot === rightRoot) {
      return;
    }
    if (this.rank[leftRoot] < this.rank[rightRoot]) {
      [leftRoot, rightRoot] = [rightRoot, leftRoot];
    }
    this.parent[rightRoot] = leftRoot;
    if (this.rank[leftRoot] === this.rank[rightRoot]) {
      this.rank[leftRoot] += 1;
    }
    this.componentCount -= 1;
  }

  components(): number {
    return this.componentCount;
  }
}
