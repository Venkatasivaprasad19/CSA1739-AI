
from itertools import permutations

cities = ["A", "B", "C", "D", "E"]
dist = [            # symmetric distance matrix (km)
    [0, 5, 3, 6, 17],
    [5, 0, 8, 10, 15],
    [3, 8, 0, 11, 15],
    [6, 10, 11, 0, 18],
    [17, 15, 15, 18, 0],
]


def tour_cost(tour):
    cost = 0
    for i in range(len(tour)):
        cost += dist[tour[i]][tour[(i + 1) % len(tour)]]   # last -> back to start
    return cost


def brute_force(start=0):
    others = [c for c in range(len(cities)) if c != start]
    best_tour, best_cost, count = None, float("inf"), 0
    for perm in permutations(others):
        tour = (start,) + perm
        count += 1
        cost = tour_cost(tour)
        if cost < best_cost:
            best_tour, best_cost = tour, cost
    return best_tour, best_cost, count


def nearest_neighbour(start=0):
    unvisited = set(range(len(cities))) - {start}
    tour = [start]
    while unvisited:
        nxt = min(unvisited, key=lambda c: dist[tour[-1]][c])
        tour.append(nxt)
        unvisited.remove(nxt)
    return tuple(tour), tour_cost(tour)


def name(tour):
    return " -> ".join(cities[c] for c in tour) + " -> " + cities[tour[0]]


if __name__ == "__main__":
    print("TRAVELLING SALESMAN PROBLEM\n")
    print("Distance matrix (km):")
    print("    " + "".join(f"{c:>4}" for c in cities))
    for i, row in enumerate(dist):
        print(f"{cities[i]:>3} " + "".join(f"{d:>4}" for d in row))

    best, cost, count = brute_force()
    print(f"\nBrute force checked {count} tours")
    print("Optimal tour :", name(best))
    print("Minimum cost :", cost, "km")

    nn, nn_cost = nearest_neighbour()
    print("\nNearest-neighbour tour :", name(nn))
    print("Cost                   :", nn_cost, "km")
