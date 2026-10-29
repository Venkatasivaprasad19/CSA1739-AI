
import math
import random

random.seed(1)                       # same result every time you run


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


class NeuralNetwork:
    def __init__(self, n_in, n_hidden, n_out, lr=0.5):
        self.lr = lr
        rnd = lambda: random.uniform(-1, 1)
        self.w1 = [[rnd() for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [rnd() for _ in range(n_hidden)]
        self.w2 = [[rnd() for _ in range(n_hidden)] for _ in range(n_out)]
        self.b2 = [rnd() for _ in range(n_out)]

    def forward(self, x):
        self.x = x
        self.h = [sigmoid(sum(w * xi for w, xi in zip(row, x)) + b)
                  for row, b in zip(self.w1, self.b1)]
        self.o = [sigmoid(sum(w * hi for w, hi in zip(row, self.h)) + b)
                  for row, b in zip(self.w2, self.b2)]
        return self.o

    def backward(self, target):
        # output layer error term (delta)
        d_out = [(o - t) * o * (1 - o) for o, t in zip(self.o, target)]
        # hidden layer error term
        d_hid = [self.h[j] * (1 - self.h[j]) *
                 sum(d_out[k] * self.w2[k][j] for k in range(len(d_out)))
                 for j in range(len(self.h))]
        # update weights and biases
        for k in range(len(self.w2)):
            for j in range(len(self.h)):
                self.w2[k][j] -= self.lr * d_out[k] * self.h[j]
            self.b2[k] -= self.lr * d_out[k]
        for j in range(len(self.w1)):
            for i in range(len(self.x)):
                self.w1[j][i] -= self.lr * d_hid[j] * self.x[i]
            self.b1[j] -= self.lr * d_hid[j]

    def train(self, data, epochs):
        for epoch in range(1, epochs + 1):
            error = 0.0
            for x, t in data:
                out = self.forward(x)
                error += 0.5 * sum((o - ti) ** 2 for o, ti in zip(out, t))
                self.backward(t)
            if epoch == 1 or epoch % 1000 == 0:
                print(f"Epoch {epoch:>5}   error = {error:.6f}")


if __name__ == "__main__":
    xor_data = [([0, 0], [0]), ([0, 1], [1]), ([1, 0], [1]), ([1, 1], [0])]

    print("FEED FORWARD NEURAL NETWORK (2-3-1) LEARNING XOR\n")
    net = NeuralNetwork(2, 3, 1, lr=0.5)

    print("Before training:")
    for x, t in xor_data:
        print(f"  Input {x} -> output {net.forward(x)[0]:.4f}   (target {t[0]})")

    print("\nTraining...")
    net.train(xor_data, epochs=10000)

    print("\nAfter training:")
    for x, t in xor_data:
        out = net.forward(x)[0]
        print(f"  Input {x} -> output {out:.4f}  -> predicted {round(out)}   (target {t[0]})")

    print("\nLearned weights")
    print("  Input -> Hidden :", [[round(w, 3) for w in r] for r in net.w1])
    print("  Hidden biases   :", [round(b, 3) for b in net.b1])
    print("  Hidden -> Output:", [[round(w, 3) for w in r] for r in net.w2])
    print("  Output bias     :", [round(b, 3) for b in net.b2])
