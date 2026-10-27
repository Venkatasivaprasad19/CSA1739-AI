
N = 8


def is_safe(rows, col, row):
    """rows[c] = row of the queen in column c (for columns 0..col-1)."""
    for c in range(col):
        r = rows[c]
        if r == row or abs(r - row) == abs(c - col):   # same row / diagonal
            return False
    return True


def solve(col, rows, solutions):
    if col == N:
        solutions.append(rows[:])
        return
    for row in range(N):
        if is_safe(rows, col, row):
            rows.append(row)
            solve(col + 1, rows, solutions)
            rows.pop()                                  # backtrack


def print_board(rows):
    for r in range(N):
        print(" ".join("Q" if rows[c] == r else "." for c in range(N)))
    print()


if __name__ == "__main__":
    solutions = []
    solve(0, [], solutions)

    print("8-QUEENS USING BACKTRACKING\n")
    print("Total number of solutions:", len(solutions), "\n")
    print("First solution (row number of the queen in columns 1..8):",
          [r + 1 for r in solutions[0]], "\n")
    print_board(solutions[0])
    print("Second solution:", [r + 1 for r in solutions[1]], "\n")
    print_board(solutions[1])
