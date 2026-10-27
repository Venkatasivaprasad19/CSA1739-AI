
from collections import deque
from math import gcd


def next_states(state, cap1, cap2):
    x, y = state
    return [
        ("Fill jug 1",           (cap1, y)),
        ("Fill jug 2",           (x, cap2)),
        ("Empty jug 1",          (0, y)),
        ("Empty jug 2",          (x, 0)),
        ("Pour jug 1 -> jug 2",  (x - min(x, cap2 - y), y + min(x, cap2 - y))),
        ("Pour jug 2 -> jug 1",  (x + min(y, cap1 - x), y - min(y, cap1 - x))),
    ]


def water_jug(cap1, cap2, target):
    if target > max(cap1, cap2) or target % gcd(cap1, cap2) != 0:
        return None                                  # impossible
    start = (0, 0)
    queue = deque([start])
    parent = {start: (None, "Start")}
    while queue:
        cur = queue.popleft()
        if cur[0] == target or cur[1] == target:     # goal test
            path = []
            while cur is not None:
                prev, action = parent[cur]
                path.append((action, cur))
                cur = prev
            return path[::-1]
        for action, nxt in next_states(cur, cap1, cap2):
            if nxt not in parent:
                parent[nxt] = (cur, action)
                queue.append(nxt)
    return None


if __name__ == "__main__":
    CAP1, CAP2, TARGET = 4, 3, 2          # change values to try other jugs
    print(f"WATER JUG PROBLEM: jugs {CAP1}L and {CAP2}L, target {TARGET}L\n")
    result = water_jug(CAP1, CAP2, TARGET)
    if result is None:
        print("No solution possible.")
    else:
        print(f"{'Step':<5}{'Action':<24}{'State (x, y)'}")
        for i, (action, state) in enumerate(result):
            print(f"{i:<5}{action:<24}{state}")
        print(f"\nSolved in {len(result) - 1} moves.")
