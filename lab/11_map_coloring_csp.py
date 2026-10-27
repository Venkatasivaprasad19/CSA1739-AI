
# Map of Australia (the classic textbook example)
neighbors = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "Q"],
    "SA":  ["WA", "NT", "Q", "NSW", "V"],
    "Q":   ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V":   ["SA", "NSW"],
    "T":   [],
}

nodes_visited = 0


def is_consistent(region, colour, assignment):
    """Check the constraint: no neighbour already has the same colour."""
    return all(assignment.get(nb) != colour for nb in neighbors[region])


def select_unassigned(assignment, domains):
    """MRV: region with the smallest number of legal colours left."""
    unassigned = [r for r in neighbors if r not in assignment]
    return min(unassigned, key=lambda r: (len(domains[r]), -len(neighbors[r])))


def backtrack(assignment, domains):
    global nodes_visited
    if len(assignment) == len(neighbors):          # all regions coloured
        return assignment
    region = select_unassigned(assignment, domains)
    for colour in domains[region]:
        nodes_visited += 1
        if is_consistent(region, colour, assignment):
            assignment[region] = colour
            # forward checking: copy domains and remove colour from neighbours
            new_domains = {r: list(d) for r, d in domains.items()}
            ok = True
            for nb in neighbors[region]:
                if nb not in assignment and colour in new_domains[nb]:
                    new_domains[nb].remove(colour)
                    if not new_domains[nb]:         # a neighbour has no colour left
                        ok = False
                        break
            if ok:
                result = backtrack(assignment, new_domains)
                if result is not None:
                    return result
            del assignment[region]                  # backtrack
    return None


def solve(colours):
    global nodes_visited
    nodes_visited = 0
    domains = {region: list(colours) for region in neighbors}
    return backtrack({}, domains)


def verify(solution):
    return all(solution[a] != solution[b] for a in neighbors for b in neighbors[a])


if __name__ == "__main__":
    print("MAP COLORING USING CSP (BACKTRACKING + MRV + FORWARD CHECKING)\n")
    print("Regions and their neighbours:")
    for region, nbs in neighbors.items():
        print(f"  {region:<4} -> {', '.join(nbs) if nbs else '(no neighbours)'}")

    for colours in (["Red", "Green", "Blue"], ["Red", "Green"]):
        print(f"\nTrying with {len(colours)} colours: {colours}")
        solution = solve(colours)
        if solution is None:
            print("  No solution exists with these colours.")
        else:
            for region in neighbors:
                print(f"  {region:<4} = {solution[region]}")
            print("  All constraints satisfied:", verify(solution))
        print("  Assignments tried:", nodes_visited)
