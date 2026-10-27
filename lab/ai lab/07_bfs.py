
from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}


def bfs_traversal(graph, start):
    visited = [start]
    queue = deque([start])
    while queue:
        node = queue.popleft()
        print(f"Visit {node:<2} queue = {list(queue)}")
        for nb in graph[node]:
            if nb not in visited:
                visited.append(nb)
                queue.append(nb)
    return visited


def bfs_shortest_path(graph, start, goal):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append(path + [nb])
    return None


if __name__ == "__main__":
    print("BREADTH-FIRST SEARCH\n")
    print("Graph (adjacency list):")
    for k, v in graph.items():
        print(f"  {k} -> {v}")
    print("\nTraversal from A:")
    order = bfs_traversal(graph, "A")
    print("\nBFS order :", " -> ".join(order))
    path = bfs_shortest_path(graph, "A", "G")
    print("Shortest path A to G :", " -> ".join(path), f"({len(path) - 1} edges)")
