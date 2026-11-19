"""
Program 3 : Reinforcement Learning agent for a basic game (CO2)
Aim   : Train an agent with Q-learning to walk from Start (S) to Goal (G)
        in a 4 x 4 grid world (FrozenLake style) without falling in a hole (H).
Idea  : The agent learns a Q-table  Q[state][action]  from rewards:
            Q(s,a) = Q(s,a) + alpha * ( r + gamma * max Q(s',a') - Q(s,a) )
        It explores with epsilon-greedy (random move with probability epsilon).
Rewards : +1 reaching the goal, -1 falling in a hole, -0.01 for each step.
Needs   : Python only (no installation).
"""
import random

MAP = ["SFFF",
       "FHFH",
       "FFFH",
       "HFFG"]
ROWS, COLS = len(MAP), len(MAP[0])
ACTIONS = ["Up", "Down", "Left", "Right"]
ARROWS = {0: "^", 1: "v", 2: "<", 3: ">"}
MOVES = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}


class GridWorld:
    def __init__(self):
        self.state = (0, 0)

    def reset(self):
        self.state = (0, 0)
        return self.state

    def step(self, action):
        r, c = self.state
        dr, dc = MOVES[action]
        nr, nc = min(max(r + dr, 0), ROWS - 1), min(max(c + dc, 0), COLS - 1)
        self.state = (nr, nc)
        cell = MAP[nr][nc]
        if cell == "G":
            return self.state, 1.0, True
        if cell == "H":
            return self.state, -1.0, True
        return self.state, -0.01, False


def train(episodes=3000, alpha=0.5, gamma=0.95, eps_start=1.0, eps_end=0.05):
    env = GridWorld()
    Q = {(r, c): [0.0] * 4 for r in range(ROWS) for c in range(COLS)}
    history = []
    for ep in range(episodes):
        eps = max(eps_end, eps_start - ep / (0.7 * episodes))        # decay exploration
        s, done, total = env.reset(), False, 0.0
        for _ in range(100):
            if random.random() < eps:
                a = random.randrange(4)                                # explore
            else:
                best = max(Q[s])
                a = random.choice([i for i, q in enumerate(Q[s]) if q == best])   # exploit
            s2, reward, done = env.step(a)
            Q[s][a] += alpha * (reward + gamma * max(Q[s2]) * (not done) - Q[s][a])
            s, total = s2, total + reward
            if done:
                break
        history.append(total)
        if (ep + 1) % 500 == 0:
            avg = sum(history[-500:]) / 500
            print(f"Episode {ep + 1:>5}   epsilon = {eps:.2f}   average reward (last 500) = {avg:6.3f}")
    return Q


def show_policy(Q):
    print("\nLearned policy (arrow = best action in each cell):")
    for r in range(ROWS):
        row = ""
        for c in range(COLS):
            if MAP[r][c] in "GH":
                row += f" {MAP[r][c]} "
            else:
                q = Q[(r, c)]
                row += f" {ARROWS[q.index(max(q))]} "
        print("   " + row)


def play_greedy(Q, games=100):
    env, wins = GridWorld(), 0
    path = []
    for g in range(games):
        s, done, steps, trail = env.reset(), False, 0, [(0, 0)]
        while not done and steps < 50:
            a = Q[s].index(max(Q[s]))
            s, reward, done = env.step(a)
            trail.append(s)
            steps += 1
        if MAP[s[0]][s[1]] == "G":
            wins += 1
        if g == 0:
            path = trail
    return wins, path


if __name__ == "__main__":
    random.seed(7)
    print("Q-LEARNING AGENT ON A 4x4 GRID WORLD\n")
    for row in MAP:
        print("   ", " ".join(row))
    print("    S = start, F = frozen (safe), H = hole, G = goal\n")
    Q = train()
    show_policy(Q)
    wins, path = play_greedy(Q)
    print(f"\nGreedy agent reached the goal in {wins} of 100 games")
    print("Path taken :", " -> ".join(f"({r},{c})" for r, c in path))
    print(f"Number of steps : {len(path) - 1} (shortest possible = 6)")
