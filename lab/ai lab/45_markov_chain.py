"""
Program 5 : Markov Chain model for predicting sequences of events (CO3)
Aim   : Learn the probability of moving from one state to the next from
        observed data, then predict the next event(s).
Markov property : the next state depends only on the CURRENT state.
Part A : Weather sequence (Sunny / Cloudy / Rainy)
Part B : Next-word prediction from text
Install : pip install numpy
"""
import random
from collections import defaultdict, Counter
import numpy as np

STATES = ["Sunny", "Cloudy", "Rainy"]


def generate_observations(n_days=300, seed=3):
    """Pretend we recorded the weather for n_days (true matrix is unknown to the model)."""
    true_P = np.array([[0.70, 0.20, 0.10],
                       [0.30, 0.40, 0.30],
                       [0.20, 0.30, 0.50]])
    rng = np.random.default_rng(seed)
    seq, s = [], 0
    for _ in range(n_days):
        seq.append(STATES[s])
        s = rng.choice(3, p=true_P[s])
    return seq, true_P


def estimate_matrix(seq):
    idx = {s: i for i, s in enumerate(STATES)}
    counts = np.zeros((3, 3))
    for a, b in zip(seq[:-1], seq[1:]):
        counts[idx[a], idx[b]] += 1
    return counts, counts / counts.sum(axis=1, keepdims=True)


def print_matrix(P, title, fmt=".3f"):
    print(title)
    print(f"{'':>8}" + "".join(f"{s:>9}" for s in STATES))
    for i, s in enumerate(STATES):
        print(f"{s:>8}" + "".join(f"{P[i, j]:>9{fmt}}" for j in range(3)))
    print()


def stationary(P):
    vals, vecs = np.linalg.eig(P.T)
    v = np.real(vecs[:, np.argmin(abs(vals - 1))])
    return v / v.sum()


def simulate(P, start, n, rng):
    s, out = STATES.index(start), [start]
    for _ in range(n):
        s = rng.choice(3, p=P[s])
        out.append(STATES[s])
    return out


# ----------------- Part B : text -----------------
TEXT = ("the student studies the algorithm and the student writes the program "
        "the program runs on the computer and the computer prints the result "
        "the teacher checks the program and the student improves the algorithm")


def build_word_chain(text):
    words = text.split()
    chain = defaultdict(Counter)
    for a, b in zip(words[:-1], words[1:]):
        chain[a][b] += 1
    return chain


if __name__ == "__main__":
    print("PART A : WEATHER MARKOV CHAIN\n")
    seq, true_P = generate_observations()
    print("First 15 observed days :", ", ".join(seq[:15]), "...\n")
    counts, P = estimate_matrix(seq)
    print("Transition counts learned from", len(seq), "days:")
    print_matrix(counts, "", fmt=".0f")
    print_matrix(P, "Estimated transition probability matrix P(next | today):")
    print_matrix(true_P, "(True matrix used to generate the data, for comparison):")

    today = "Sunny"
    row = P[STATES.index(today)]
    print(f"Today is {today}. Tomorrow's probabilities: " +
          ", ".join(f"{s} {p:.0%}" for s, p in zip(STATES, row)))
    print(f"Most likely tomorrow : {STATES[int(row.argmax())]}\n")

    for n in (2, 3, 7):
        Pn = np.linalg.matrix_power(P, n)[STATES.index(today)]
        print(f"After {n} days from {today} : " + ", ".join(f"{s} {p:.1%}" for s, p in zip(STATES, Pn)))
    pi = stationary(P)
    print("\nLong-run (stationary) distribution : " + ", ".join(f"{s} {p:.1%}" for s, p in zip(STATES, pi)))

    rng = np.random.default_rng(10)
    print("\nSimulated forecast for the next 10 days starting from Cloudy:")
    print("  " + " -> ".join(simulate(P, "Cloudy", 10, rng)))

    print("\n" + "=" * 60)
    print("PART B : NEXT-WORD PREDICTION WITH A MARKOV CHAIN\n")
    chain = build_word_chain(TEXT)
    for w in ("the", "student", "program"):
        total = sum(chain[w].values())
        top = chain[w].most_common(3)
        print(f"After '{w}' : " + ", ".join(f"{nxt} ({c / total:.0%})" for nxt, c in top))
    random.seed(4)
    word, sentence = "the", ["the"]
    for _ in range(9):
        options = chain[word]
        word = random.choices(list(options), weights=list(options.values()))[0]
        sentence.append(word)
    print("\nGenerated text :", " ".join(sentence))
