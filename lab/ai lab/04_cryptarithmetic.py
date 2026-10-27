
from itertools import permutations


def solve(word1, word2, result):
    letters = sorted(set(word1 + word2 + result))
    if len(letters) > 10:
        return None
    first = {word1[0], word2[0], result[0]}          # cannot be zero

    def value(word, mapping):
        n = 0
        for ch in word:
            n = n * 10 + mapping[ch]
        return n

    for digits in permutations(range(10), len(letters)):
        mapping = dict(zip(letters, digits))
        if any(mapping[ch] == 0 for ch in first):
            continue
        if value(word1, mapping) + value(word2, mapping) == value(result, mapping):
            return mapping
    return None


if __name__ == "__main__":
    puzzles = [("SEND", "MORE", "MONEY"),
               ("TO", "GO", "OUT"),
               ("BASE", "BALL", "GAMES")]
    print("CRYPT-ARITHMETIC PROBLEM\n")
    for w1, w2, res in puzzles:
        m = solve(w1, w2, res)
        print(f"{w1} + {w2} = {res}")
        if m is None:
            print("   No solution\n")
            continue
        print("   Letter -> digit :", dict(sorted(m.items())))
        n1 = "".join(str(m[c]) for c in w1)
        n2 = "".join(str(m[c]) for c in w2)
        nr = "".join(str(m[c]) for c in res)
        print(f"   {n1} + {n2} = {nr}\n")
