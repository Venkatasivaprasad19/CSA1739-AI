


tree = [
    [[3, 5], [6, 9]],        # left subtree  (MIN node with two MAX children)
    [[1, 2], [0, -1]],       # right subtree
]

leaf_count = 0               # number of leaf nodes evaluated


def minimax(node, depth, is_max, name="Root"):
    """Return the minimax value of 'node'."""
    global leaf_count
    indent = "    " * depth
    if not isinstance(node, list):                  # leaf node
        leaf_count += 1
        print(f"{indent}Leaf reached, value = {node}")
        return node

    player = "MAX" if is_max else "MIN"
    print(f"{indent}{name} ({player}) node")
    if is_max:
        best = float("-inf")
        for i, child in enumerate(node):
            val = minimax(child, depth + 1, False, f"{name}.{i}")
            best = max(best, val)
        print(f"{indent}{name} (MAX) value = {best}")
    else:
        best = float("inf")
        for i, child in enumerate(node):
            val = minimax(child, depth + 1, True, f"{name}.{i}")
            best = min(best, val)
        print(f"{indent}{name} (MIN) value = {best}")
    return best


def best_move(root):
    """Which child of the root (MAX) should be chosen?"""
    values = [minimax(child, 1, False, f"Root.{i}") for i, child in enumerate(root)]
    return values.index(max(values)), values


if __name__ == "__main__":
    print("MINIMAX ALGORITHM\n")
    print("Game tree:", tree, "\n")
    result = minimax(tree, 0, True)
    print("\nMinimax value of the root =", result)
    print("Leaf nodes evaluated      =", leaf_count)

    leaf_count = 0
    print("\nChoosing the best move at the root (silent run):")
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        move, values = best_move(tree)
    print("Values of the root's children :", values)
    side = "left" if move == 0 else "right"
    print(f"Best move for MAX             : branch {move} ({side})")
