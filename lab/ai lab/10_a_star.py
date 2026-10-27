"""
Experiment 10 : A* Algorithm  (CO4)
Aim   : Find the least-cost path using f(n) = g(n) + h(n)
        g(n) = cost from start to n, h(n) = heuristic estimate from n to goal.
        A priority queue (heapq) always expands the node with the smallest f.
The heuristic below never over-estimates (admissible), so A* is optimal.
"""
import heapq

graph = {                       # undirected weighted graph
    "S": {"A": 1, "B": 4},
    "A": {"S": 1, "B": 2, "C": 5, "D": 12},
    "B": {"S": 4, "A": 2, "C": 2},
    "C": {"A": 5, "B": 2, "D": 3, "G": 7},
    "D": {"A": 12, "C": 3, "G": 3},
    "G": {"C": 7, "D": 3},
}

h = {"S": 9, "A": 8, "B": 6, "C": 5, "D": 2, "G": 0}    # heuristic values


def a_star(start, goal):
    open_list = [(h[start], 0, start, [start])]          # (f, g, node, path)
    best_g = {start: 0}
    step = 1
    while open_list:
        f, g, node, path = heapq.heappop(open_list)
        if g > best_g[node]:                 # outdated (more costly) entry
            continue
        print(f"Step {step}: expand {node}  g={g} h={h[node]} f={f}  "
              f"path={'->'.join(path)}")
        step += 1
        if node == goal:
            return path, g
        for nb, cost in graph[node].items():
            new_g = g + cost
            if nb not in best_g or new_g < best_g[nb]:
                best_g[nb] = new_g
                heapq.heappush(open_list,
                               (new_g + h[nb], new_g, nb, path + [nb]))
    return None, float("inf")


if __name__ == "__main__":
    print("A* ALGORITHM\n")
    print("Heuristic h(n):", h, "\n")
    path, cost = a_star("S", "G")
    print("\nShortest path :", " -> ".join(path))
    print("Total cost    :", cost)
