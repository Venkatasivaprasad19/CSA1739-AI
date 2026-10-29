tree = [
    [[3, 5], [6, 9]],
    [[1, 2], [0, -1]],
]

alpha_beta_leaves = 0
minimax_leaves = 0


def minimax(node, is_max):
    """Plain minimax, used only to compare the number of leaf evaluations."""
    global minimax_leaves
    if not isinstance(node, list):
        minimax_leaves += 1
        return node
    values = [minimax(c, not is_max) for c in node]
    return max(values) if is_max else min(values)


def alpha_beta(node, depth, alpha, beta, is_max, name="Root"):
    global alpha_beta_leaves
    indent = "    " * depth
    if not isinstance(node, list):
        alpha_beta_leaves += 1
        print(f"{indent}Leaf value = {node}")
        return node

    player = "MAX" if is_max else "MIN"
    print(f"{indent}{name} ({player})  alpha={alpha} beta={beta}")
    if is_max:
        best = float("-inf")
        for i, child in enumerate(node):
            val = alpha_beta(child, depth + 1, alpha, beta, False, f"{name}.{i}")
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                remaining = len(node) - i - 1
                if remaining:
                    print(f"{indent}  PRUNED {remaining} branch(es) of {name} "
                          f"(alpha={alpha} >= beta={beta})")
                break
        return best
    else:
        best = float("inf")
        for i, child in enumerate(node):
            val = alpha_beta(child, depth + 1, alpha, beta, True, f"{name}.{i}")
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                remaining = len(node) - i - 1
                if remaining:
                    print(f"{indent}  PRUNED {remaining} branch(es) of {name} "
                          f"(alpha={alpha} >= beta={beta})")
                break
        return best


if __name__ == "__main__":
    print("ALPHA-BETA PRUNING\n")
    print("Game tree:", tree, "\n")
    value = alpha_beta(tree, 0, float("-inf"), float("inf"), True)
    print("\nValue of the root (alpha-beta) =", value)

    same = minimax(tree, True)
    print("Value of the root (minimax)    =", same)
    print("\nLeaf nodes evaluated by minimax    :", minimax_leaves)
    print("Leaf nodes evaluated by alpha-beta :", alpha_beta_leaves)
    print("Leaf nodes saved by pruning        :", minimax_leaves - alpha_beta_leaves)
