"""
Program 2 : K-Means Clustering (CO2)
Aim   : Group similar data points (customers) into clusters.
Data  : 300 synthetic customers with two features
        (annual income in k$, spending score 1-100).
Steps : 1. K-Means written from scratch (k-means++ start, assign, update, repeat)
        2. Elbow method (inertia) and silhouette score to choose the best k
        3. Final clusters printed and plotted
Install : pip install numpy matplotlib
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def make_data(seed=42):
    rng = np.random.default_rng(seed)
    centers = [(25, 20), (25, 80), (55, 50), (85, 20), (85, 80)]
    X = np.vstack([rng.normal(c, 6, size=(60, 2)) for c in centers])
    return X


def kmeans(X, k, max_iter=100, seed=0):
    rng = np.random.default_rng(seed)
    # k-means++ initialisation: choose far-apart starting centroids
    centroids = [X[rng.integers(len(X))]]
    for _ in range(1, k):
        d2 = np.min(((X[:, None, :] - np.array(centroids)[None, :, :]) ** 2).sum(axis=2), axis=1)
        centroids.append(X[rng.choice(len(X), p=d2 / d2.sum())])
    centroids = np.array(centroids)

    for iteration in range(1, max_iter + 1):
        # assignment step: nearest centroid for every point
        dist = ((X[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
        labels = dist.argmin(axis=1)
        # update step: move every centroid to the mean of its points
        new = np.array([X[labels == j].mean(axis=0) if np.any(labels == j) else centroids[j]
                        for j in range(k)])
        shift = np.linalg.norm(new - centroids)
        centroids = new
        if shift < 1e-6:                      # converged
            break
    inertia = ((X - centroids[labels]) ** 2).sum()
    return labels, centroids, inertia, iteration


def silhouette(X, labels):
    """Average silhouette score (closer to 1 = well separated clusters)."""
    n = len(X)
    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
    scores = []
    for i in range(n):
        same = (labels == labels[i])
        same[i] = False
        if not same.any():
            scores.append(0.0)
            continue
        a = D[i, same].mean()
        b = min(D[i, labels == c].mean() for c in set(labels) if c != labels[i])
        scores.append((b - a) / max(a, b))
    return float(np.mean(scores))


def show(fig_name):
    plt.savefig(os.path.join(OUT_DIR, fig_name), dpi=120, bbox_inches="tight")
    if matplotlib.get_backend().lower() != "agg":
        plt.show()
    plt.close()


if __name__ == "__main__":
    X = make_data()
    print("K-MEANS CLUSTERING OF CUSTOMERS")
    print("Data points :", X.shape[0], "  Features: income (k$), spending score\n")

    # ---- choose k with elbow + silhouette ----
    ks = range(2, 9)
    results = {}
    print(f"{'k':>2} {'inertia':>10} {'silhouette':>11} {'iterations':>11}")
    for k in ks:
        labels, cents, inertia, iters = kmeans(X, k)
        sil = silhouette(X, labels)
        results[k] = (inertia, sil)
        print(f"{k:>2} {inertia:>10.1f} {sil:>11.3f} {iters:>11}")
    best_k = max(results, key=lambda k: results[k][1])
    print(f"\nBest number of clusters (highest silhouette) : k = {best_k}")

    plt.figure(figsize=(5, 3.5))
    plt.plot(list(ks), [results[k][0] for k in ks], "o-")
    plt.axvline(best_k, color="red", linestyle="--", label=f"chosen k = {best_k}")
    plt.xlabel("number of clusters k")
    plt.ylabel("inertia (within-cluster sum of squares)")
    plt.title("Elbow method")
    plt.legend()
    show("kmeans_elbow.png")

    # ---- final clustering ----
    labels, cents, inertia, iters = kmeans(X, best_k)
    print(f"\nFinal clustering converged in {iters} iterations, inertia = {inertia:.1f}\n")
    print(f"{'Cluster':<8}{'Customers':>10}   Centroid (income, spending)")
    for j in range(best_k):
        print(f"{j:<8}{int((labels == j).sum()):>10}   ({cents[j][0]:.1f}, {cents[j][1]:.1f})")

    plt.figure(figsize=(6, 4.5))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="tab10", s=25)
    plt.scatter(cents[:, 0], cents[:, 1], c="black", marker="X", s=200, label="centroids")
    plt.xlabel("Annual income (k$)")
    plt.ylabel("Spending score")
    plt.title(f"K-Means result (k = {best_k})")
    plt.legend()
    show("kmeans_clusters.png")
    print("\nPlots saved: kmeans_elbow.png, kmeans_clusters.png")
