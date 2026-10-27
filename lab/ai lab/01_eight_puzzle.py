"""
Experiment 1 : 8-Puzzle Problem  (CO1)
Aim   : Solve the 8-puzzle using Breadth-First Search (uninformed search),
        which always gives the solution with the minimum number of moves.
State : a tuple of 9 numbers (row by row), 0 represents the blank.
"""
from collections import deque

GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


def is_solvable(state):
    """Half of all 8-puzzle states cannot reach the goal. Check inversions."""
    tiles = [x for x in state if x != 0]
    inversions = sum(1 for i in range(len(tiles))
                     for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
    return inversions % 2 == 0


def get_neighbors(state):
    """Generate (move, new_state) by sliding the blank Up/Down/Left/Right."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    for move, dr, dc in (("Up", -1, 0), ("Down", 1, 0),
                         ("Left", 0, -1), ("Right", 0, 1)):
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new = nr * 3 + nc
            s = list(state)
            s[blank], s[new] = s[new], s[blank]
            yield move, tuple(s)


def bfs(start):
    queue = deque([start])
    parent = {start: (None, None)}          # state -> (previous state, move)
    expanded = 0
    while queue:
        current = queue.popleft()
        expanded += 1
        if current == GOAL:
            path = []
            while parent[current][0] is not None:
                prev, move = parent[current]
                path.append((move, current))
                current = prev
            path.reverse()
            return path, expanded
        for move, nxt in get_neighbors(current):
            if nxt not in parent:
                parent[nxt] = (current, move)
                queue.append(nxt)
    return None, expanded


def show(state):
    for i in range(0, 9, 3):
        print(" ".join(str(x) if x else "_" for x in state[i:i + 3]))
    print()


if __name__ == "__main__":
    start = (8, 1, 3,
             4, 0, 2,
             7, 6, 5)                          # change this to try other puzzles

    print("8-PUZZLE USING BREADTH-FIRST SEARCH\n")
    print("Initial state:")
    show(start)
    print("Goal state:")
    show(GOAL)

    if not is_solvable(start):
        print("This puzzle is NOT solvable.")
    else:
        solution, expanded = bfs(start)
        print(f"Solution found in {len(solution)} moves "
              f"({expanded} states expanded)\n")
        for i, (move, state) in enumerate(solution, 1):
            print(f"Step {i}: move blank {move}")
            show(state)
