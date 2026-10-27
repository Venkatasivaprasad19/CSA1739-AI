
graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}


def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = []
    visited.append(node)
    for nb in graph[node]:
        if nb not in visited:
            dfs_recursive(graph, nb, visited)
    return visited


def dfs_iterative(graph, start):
    visited, stack = [], [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            print(f"Visit {node:<2} stack = {stack}")
            # reversed() so that the left-most neighbour is explored first
            for nb in reversed(graph[node]):
                if nb not in visited:
                    stack.append(nb)
    return visited


def dfs_path(graph, node, goal, path=None):
    path = (path or []) + [node]
    if node == goal:
        return path
    for nb in graph[node]:
        if nb not in path:
            found = dfs_path(graph, nb, goal, path)
            if found:
                return found
    return None


if __name__ == "__main__":
    print("DEPTH-FIRST SEARCH\n")
    print("Recursive DFS from A :", " -> ".join(dfs_recursive(graph, "A")))
    print("\nIterative DFS from A (using a stack):")
    order = dfs_iterative(graph, "A")
    print("\nIterative DFS order  :", " -> ".join(order))
    print("A path from A to G   :", " -> ".join(dfs_path(graph, "A", "G")))
