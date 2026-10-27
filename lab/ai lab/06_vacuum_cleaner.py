
import itertools


def reflex_vacuum_agent(percept):
    location, status = percept
    if status == "Dirty":
        return "Suck"
    return "Right" if location == "A" else "Left"


def run(env, location, steps=6, verbose=True):
    score = 0
    if verbose:
        print(f"{'Step':<6}{'Location':<10}{'Percept':<20}{'Action':<8}"
              f"{'A':<8}{'B':<8}Score")
    for t in range(1, steps + 1):
        percept = (location, env[location])
        action = reflex_vacuum_agent(percept)
        if action == "Suck":
            env[location] = "Clean"
        elif action == "Right":
            location = "B"
            score -= 1
        else:
            location = "A"
            score -= 1
        score += sum(1 for room in env.values() if room == "Clean")
        if verbose:
            print(f"{t:<6}{location:<10}{str(percept):<20}{action:<8}"
                  f"{env['A']:<8}{env['B']:<8}{score}")
    return score


if __name__ == "__main__":
    print("VACUUM CLEANER (SIMPLE REFLEX AGENT)\n")
    print("Detailed run: start in A, both rooms dirty\n")
    run({"A": "Dirty", "B": "Dirty"}, "A")

    print("\nPerformance for every possible starting situation (6 steps):\n")
    print(f"{'Start room':<12}{'Room A':<10}{'Room B':<10}Score")
    for loc, a, b in itertools.product("AB", ("Clean", "Dirty"), ("Clean", "Dirty")):
        s = run({"A": a, "B": b}, loc, verbose=False)
        print(f"{loc:<12}{a:<10}{b:<10}{s}")
