"""Independent, untimed reference results for the application comparison."""

from collections import Counter, deque

MODULUS = 1_000_000_007
TITLES = [
    "Война и мир",
    "Мастер и Маргарита",
    "Ёжик в тумане",
    "Книга моря",
    "Белый парус",
    "Путь домой",
    "Сад камней",
    "Зимняя ночь",
    "The Go Book",
    "Rust in Action",
    "Marimay λ",
    "東京 🚀",
    "Книга памяти",
    "Дальний берег",
    "Тихий Дон",
    "Алые паруса",
]
LINES = [
    "книга море книга дом",
    "море свет дом книга",
    "rust go marimay go",
    "ёжик туман ёжик книга",
]


def title(index):
    return f"{TITLES[index % len(TITLES)]} #{index}"


def byte_length(text):
    return len(text.encode("utf-8"))


def state_score(index):
    return (1, index % 97 + 2, 101)[index % 3]


def expected(workload, size, rounds):
    if workload.startswith("title-search-"):
        result = sum((q * 7919 % size) + 1 for q in range(rounds) if q % 4 != 3)
    elif workload == "normalize-title":
        normalized = [
            "война и мир",
            "ёжик в тумане",
            "the go book",
            "мастер и маргарита",
        ]
        result = sum(byte_length(normalized[i % 4]) for i in range(size)) * rounds
    elif workload == "word-frequency":
        counts = Counter(word for i in range(size) for word in LINES[i % 4].split())
        result = (
            len(counts) + sum(byte_length(w) * n for w, n in counts.items())
        ) * rounds
    elif workload in ("report-builder", "report-concat"):
        data = "".join(f"{i}|{TITLES[i % 16]}|{i % 3}\n" for i in range(size)).encode(
            "utf-8"
        )
        result = sum((i % 251 + 1) * b for i, b in enumerate(data)) % MODULUS * rounds
    elif workload in ("map-int", "map-string"):
        counts = Counter((i * 25173 + 13849) % size for i in range(size * rounds))
        result = len(counts) + sum((k + 1) * v for k, v in counts.items())
    elif workload == "map-string-book":
        result = (
            sum(byte_length(title(i)) + state_score(i) + i for i in range(size))
            * rounds
        )
    elif workload == "set-string-churn":
        result = size * size * rounds + sum(
            byte_length(title(i)) for i in range(size * rounds, size * (rounds + 1))
        )
    elif workload.startswith("catalog-"):
        if workload == "catalog-match":
            result = (
                sum(state_score(i) + byte_length(TITLES[i % 16]) for i in range(size))
                * rounds
            )
        elif workload in ("catalog-dotcall", "catalog-interface"):
            result = sum(byte_length(TITLES[i % 16]) for i in range(size)) * rounds
        elif workload == "catalog-pipeline":
            counts = Counter(TITLES[i % 16] for i in range(size))
            result = sum(state_score(i) for i in range(size))
            for q in range(64):
                if q % 4 != 3:
                    index = q % 16
                    result += (index + 1 if index < size else 0) + counts[TITLES[index]]
            result *= rounds
        else:
            raise ValueError(f"unknown workload: {workload}")
    elif workload in ("record-reference-copy", "record-create"):
        result = (
            sum(
                i + byte_length(TITLES[i % 16]) + (workload == "record-reference-copy")
                for i in range(size)
            )
            * rounds
        )
    elif workload in ("array-grow", "array-reserved"):
        result = sum(i * 17 % 1009 for i in range(size)) * rounds
    elif workload in ("bfs-int", "bfs-record"):
        distances = [-1] * size
        distances[0] = 0
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            for edge in range(1, 17):
                neighbor = (vertex + edge * edge) % size
                if distances[neighbor] < 0:
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        result = sum((i + 1) * (d + 1) for i, d in enumerate(distances)) * rounds
    elif workload == "parse-result":
        result = sum(7 if i % 4 == 3 else i % 1009 + 1 for i in range(size)) * rounds
    else:
        raise ValueError(f"unknown workload: {workload}")
    return result % MODULUS
