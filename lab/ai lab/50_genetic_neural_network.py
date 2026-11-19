"""
Program 10 : Genetic Algorithm to evolve a Neural Network (CO1)
Aim   : Instead of back-propagation, EVOLVE the weights of a neural network with a
        genetic algorithm so that it solves the XOR problem
        (output 1 when the two inputs are different, otherwise 0).
Network : 2 inputs -> 3 hidden neurons (tanh) -> 1 output (sigmoid)   = 13 weights
Genetic algorithm :
        chromosome = the 13 weights          fitness = 1 / (1 + mean squared error)
        1. random population            2. evaluate fitness
        3. selection (tournament)       4. crossover (mix the weights of 2 parents)
        5. mutation (small random changes)   6. elitism (best networks survive)
        repeat for many generations until the network solves XOR.
Install : pip install numpy matplotlib
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
Y = np.array([0, 1, 1, 0], dtype=float)
N_HIDDEN = 3
N_WEIGHTS = 2 * N_HIDDEN + N_HIDDEN + N_HIDDEN + 1          # W1, b1, W2, b2 = 13


def forward(w, inputs):
    W1 = w[:6].reshape(2, N_HIDDEN)
    b1 = w[6:9]
    W2 = w[9:12]
    b2 = w[12]
    hidden = np.tanh(inputs @ W1 + b1)
    return 1.0 / (1.0 + np.exp(-(hidden @ W2 + b2)))


def fitness(w):
    mse = np.mean((forward(w, X) - Y) ** 2)
    return 1.0 / (1.0 + mse)


def evolve(pop_size=80, generations=500, elite=4, tournament=3, p_cross=0.9,
           p_mut=0.15, sigma=0.6, seed=2):
    rng = np.random.default_rng(seed)
    pop = rng.uniform(-2, 2, size=(pop_size, N_WEIGHTS))
    best_curve, mean_curve = [], []
    for gen in range(1, generations + 1):
        fit = np.array([fitness(ind) for ind in pop])
        order = np.argsort(fit)[::-1]
        pop, fit = pop[order], fit[order]
        best_curve.append(fit[0])
        mean_curve.append(fit.mean())
        pred = np.round(forward(pop[0], X))
        if gen == 1 or gen % 10 == 0:
            print(f"Generation {gen:>3}   best fitness = {fit[0]:.4f}   mean fitness = {fit.mean():.4f}   "
                  f"correct = {int((pred == Y).sum())}/4")
        if (pred == Y).all() and fit[0] > 0.99:                # solved
            print(f"\nXOR solved in generation {gen}!")
            break

        new_pop = [pop[i].copy() for i in range(elite)]          # elitism
        while len(new_pop) < pop_size:
            # tournament selection of two parents
            parents = []
            for _ in range(2):
                contenders = rng.integers(0, pop_size, tournament)
                parents.append(pop[contenders[np.argmax(fit[contenders])]])
            p1, p2 = parents
            # uniform crossover
            if rng.random() < p_cross:
                mask = rng.random(N_WEIGHTS) < 0.5
                child = np.where(mask, p1, p2)
            else:
                child = p1.copy()
            # gaussian mutation
            mutate = rng.random(N_WEIGHTS) < p_mut
            child = child + mutate * rng.normal(0, sigma, N_WEIGHTS)
            new_pop.append(child)
        pop = np.array(new_pop)
    return pop[0], best_curve, mean_curve


if __name__ == "__main__":
    print("GENETIC ALGORITHM EVOLVING A NEURAL NETWORK FOR XOR\n")
    print(f"Chromosome length (weights + biases) : {N_WEIGHTS}\n")
    best, best_curve, mean_curve = evolve()

    print("\nBest evolved network:")
    print(f"{'Input':<10}{'Output':>9}{'Predicted':>11}{'Target':>8}")
    for inp, target in zip(X, Y):
        out = forward(best, inp.reshape(1, -1))[0]
        print(f"{str(inp.astype(int)):<10}{out:>9.4f}{round(out):>11}{int(target):>8}")
    print("\nWeights :", np.round(best, 3))

    plt.figure(figsize=(6, 3.8))
    plt.plot(best_curve, label="best fitness")
    plt.plot(mean_curve, label="mean fitness")
    plt.xlabel("generation")
    plt.ylabel("fitness  1/(1+MSE)")
    plt.title("Evolution of the neural network (XOR)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(os.path.join(OUT_DIR, "ga_fitness_curve.png"), dpi=120, bbox_inches="tight")
    print("Fitness curve saved as ga_fitness_curve.png")
    if matplotlib.get_backend().lower() != "agg":
        plt.show()
