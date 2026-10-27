
from collections import deque

TOTAL_M = TOTAL_C = 3
BOAT = 2
START = (TOTAL_M, TOTAL_C, 1)
GOAL = (0, 0, 0)


def is_valid(m, c):
    if not (0 <= m <= TOTAL_M and 0 <= c <= TOTAL_C):
        return False
    mr, cr = TOTAL_M - m, TOTAL_C - c
    if m > 0 and c > m:                  # left bank unsafe
        return False
    if mr > 0 and cr > mr:               # right bank unsafe
        return False
    return True


def successors(state):
    m, c, boat = state
    sign = -1 if boat == 1 else 1        # boat leaves left -> people decrease
    for dm in range(BOAT + 1):
        for dc in range(BOAT + 1 - dm):
            if dm + dc == 0:
                continue
            nm, nc = m + sign * dm, c + sign * dc
            if is_valid(nm, nc):
                direction = "left -> right" if boat == 1 else "right -> left"
                yield (f"Move {dm}M {dc}C {direction}", (nm, nc, 1 - boat))


def bfs():
    queue = deque([START])
    parent = {START: (None, "Start")}
    while queue:
        cur = queue.popleft()
        if cur == GOAL:
            path = []
            while cur is not None:
                prev, action = parent[cur]
                path.append((action, cur))
                cur = prev
            return path[::-1]
        for action, nxt in successors(cur):
            if nxt not in parent:
                parent[nxt] = (cur, action)
                queue.append(nxt)


if __name__ == "__main__":
    print("MISSIONARIES AND CANNIBALS PROBLEM\n")
    print(f"{'Step':<5}{'Action':<26}{'Left bank (M,C)':<18}"
          f"{'Right bank (M,C)':<18}Boat")
    for i, (action, (m, c, b)) in enumerate(bfs()):
        print(f"{i:<5}{action:<26}{str((m, c)):<18}"
              f"{str((TOTAL_M - m, TOTAL_C - c)):<18}{'Left' if b else 'Right'}")
    print("\nAll 6 people crossed safely.")
