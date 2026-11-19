"""
Program 8 : Bayesian Network for probabilistic relationships (CO4)
Aim   : Model uncertain cause-and-effect relationships and answer questions such as
        "If both John and Mary call, how likely is it that there was a burglary?"
Network (classic alarm example):
        Burglary --->  Alarm  ---> JohnCalls
        Earthquake -->  Alarm  ---> MaryCalls
Each node stores a Conditional Probability Table (CPT) given its parents.
Joint probability = product of  P(variable | parents)  over all variables.
Inference method : exact inference by enumeration. Python only (no installation).
"""
from itertools import product


class BayesNet:
    def __init__(self):
        self.order = []          # variables in topological order (parents first)
        self.parents = {}
        self.cpt = {}            # cpt[var][tuple(parent values)] = P(var = True | parents)

    def add(self, var, parents, table):
        self.order.append(var)
        self.parents[var] = parents
        self.cpt[var] = table

    def p(self, var, value, assignment):
        """P(var = value | parents taken from assignment)."""
        key = tuple(assignment[pa] for pa in self.parents[var])
        p_true = self.cpt[var][key]
        return p_true if value else 1.0 - p_true

    def joint(self, assignment):
        prob = 1.0
        for var in self.order:
            prob *= self.p(var, assignment[var], assignment)
        return prob

    def _enumerate_all(self, variables, evidence):
        if not variables:
            return 1.0
        first, rest = variables[0], variables[1:]
        if first in evidence:
            return self.p(first, evidence[first], evidence) * self._enumerate_all(rest, evidence)
        total = 0.0
        for value in (True, False):
            e2 = dict(evidence)
            e2[first] = value
            total += self.p(first, value, e2) * self._enumerate_all(rest, e2)
        return total

    def query(self, var, evidence=None):
        """Return {True: P(var=True | evidence), False: ...}."""
        evidence = dict(evidence or {})
        dist = {}
        for value in (True, False):
            e = dict(evidence)
            e[var] = value
            dist[value] = self._enumerate_all(self.order, e)
        total = sum(dist.values())
        return {v: p / total for v, p in dist.items()}


def build_alarm_network():
    net = BayesNet()
    net.add("Burglary", [], {(): 0.001})
    net.add("Earthquake", [], {(): 0.002})
    net.add("Alarm", ["Burglary", "Earthquake"],
            {(True, True): 0.95, (True, False): 0.94, (False, True): 0.29, (False, False): 0.001})
    net.add("JohnCalls", ["Alarm"], {(True,): 0.90, (False,): 0.05})
    net.add("MaryCalls", ["Alarm"], {(True,): 0.70, (False,): 0.01})
    return net


def show_cpts(net):
    print("Conditional probability tables  P(variable = True | parents):\n")
    for var in net.order:
        pa = net.parents[var]
        print(f"  {var}" + (f"   (parents: {', '.join(pa)})" if pa else "   (no parents)"))
        for key, p in net.cpt[var].items():
            cond = ", ".join(f"{n}={'T' if v else 'F'}" for n, v in zip(pa, key)) or "-"
            print(f"      {cond:<28} {p}")
    print()


def ask(net, var, evidence=None):
    result = net.query(var, evidence)
    ev = ", ".join(f"{k}={'T' if v else 'F'}" for k, v in (evidence or {}).items())
    label = f"P({var}=True" + (f" | {ev})" if ev else ")")
    print(f"  {label:<55} = {result[True]:.4f}")
    return result[True]


if __name__ == "__main__":
    net = build_alarm_network()
    print("BAYESIAN NETWORK - BURGLARY / EARTHQUAKE / ALARM\n")
    show_cpts(net)

    # sanity check : the joint distribution must add up to 1
    total = sum(net.joint(dict(zip(net.order, vals))) for vals in product([True, False], repeat=5))
    print(f"Check : sum of all 32 joint probabilities = {total:.6f}\n")

    print("Joint probability example:")
    a = {"Burglary": False, "Earthquake": False, "Alarm": True, "JohnCalls": True, "MaryCalls": True}
    print(f"  P(no burglary, no earthquake, alarm rings, John calls, Mary calls) = {net.joint(a):.8f}\n")

    print("Queries (exact inference by enumeration):")
    print(" a) Prior probabilities")
    ask(net, "Alarm")
    ask(net, "JohnCalls")
    ask(net, "Burglary")
    print(" b) Diagnosis - from effects to causes")
    ask(net, "Burglary", {"JohnCalls": True})
    ask(net, "Burglary", {"JohnCalls": True, "MaryCalls": True})
    ask(net, "Earthquake", {"JohnCalls": True, "MaryCalls": True})
    print(" c) Prediction - from causes to effects")
    ask(net, "JohnCalls", {"Burglary": True})
    ask(net, "MaryCalls", {"Burglary": True, "Earthquake": False})
    print(" d) 'Explaining away' - another cause makes the first less likely")
    ask(net, "Burglary", {"Alarm": True})
    ask(net, "Burglary", {"Alarm": True, "Earthquake": True})
