
import math
from collections import Counter

ATTRIBUTES = ["Outlook", "Temperature", "Humidity", "Wind"]
DATA = [
    # Outlook,   Temp,   Humidity, Wind,    Play
    ("Sunny",    "Hot",  "High",   "Weak",   "No"),
    ("Sunny",    "Hot",  "High",   "Strong", "No"),
    ("Overcast", "Hot",  "High",   "Weak",   "Yes"),
    ("Rain",     "Mild", "High",   "Weak",   "Yes"),
    ("Rain",     "Cool", "Normal", "Weak",   "Yes"),
    ("Rain",     "Cool", "Normal", "Strong", "No"),
    ("Overcast", "Cool", "Normal", "Strong", "Yes"),
    ("Sunny",    "Mild", "High",   "Weak",   "No"),
    ("Sunny",    "Cool", "Normal", "Weak",   "Yes"),
    ("Rain",     "Mild", "Normal", "Weak",   "Yes"),
    ("Sunny",    "Mild", "Normal", "Strong", "Yes"),
    ("Overcast", "Mild", "High",   "Strong", "Yes"),
    ("Overcast", "Hot",  "Normal", "Weak",   "Yes"),
    ("Rain",     "Mild", "High",   "Strong", "No"),
]


def entropy(rows):
    counts = Counter(r[-1] for r in rows)
    total = len(rows)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def info_gain(rows, attr_index):
    total = len(rows)
    remainder = 0.0
    for value in set(r[attr_index] for r in rows):
        subset = [r for r in rows if r[attr_index] == value]
        remainder += len(subset) / total * entropy(subset)
    return entropy(rows) - remainder


def build_tree(rows, attrs):
    labels = [r[-1] for r in rows]
    if len(set(labels)) == 1:                       # pure node -> leaf
        return labels[0]
    if not attrs:                                   # no attribute left -> majority
        return Counter(labels).most_common(1)[0][0]

    best = max(attrs, key=lambda a: info_gain(rows, ATTRIBUTES.index(a)))
    idx = ATTRIBUTES.index(best)
    tree = {best: {}}
    for value in sorted(set(r[idx] for r in rows)):
        subset = [r for r in rows if r[idx] == value]
        rest = [a for a in attrs if a != best]
        tree[best][value] = build_tree(subset, rest)
    return tree


def print_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(indent + "-> " + tree)
        return
    attr = next(iter(tree))
    for value, subtree in tree[attr].items():
        if isinstance(subtree, dict):
            print(f"{indent}[{attr} = {value}]")
            print_tree(subtree, indent + "    ")
        else:
            print(f"{indent}[{attr} = {value}] -> {subtree}")


def classify(tree, example):
    while isinstance(tree, dict):
        attr = next(iter(tree))
        tree = tree[attr][example[attr]]
    return tree


if __name__ == "__main__":
    print("DECISION TREE (ID3)\n")
    print(f"Entropy of the whole data set = {entropy(DATA):.4f}\n")
    print("Information gain of each attribute at the root:")
    for i, a in enumerate(ATTRIBUTES):
        print(f"  Gain({a:<11}) = {info_gain(DATA, i):.4f}")

    tree = build_tree(DATA, ATTRIBUTES)
    print("\nDecision tree:\n")
    print_tree(tree)

    # training accuracy
    correct = sum(
        classify(tree, dict(zip(ATTRIBUTES, r[:-1]))) == r[-1] for r in DATA)
    print(f"\nTraining accuracy: {correct}/{len(DATA)}")

    print("\nClassifying new examples:")
    tests = [
        {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": "High", "Wind": "Strong"},
        {"Outlook": "Overcast", "Temperature": "Hot", "Humidity": "High", "Wind": "Weak"},
        {"Outlook": "Rain", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Strong"},
    ]
    for t in tests:
        print(" ", t, "->  Play =", classify(tree, t))
