import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def portfolio_objective(weights, returns, covariance, risk=100):
    portfolio_return = np.dot(weights, returns)
    portfolio_risk = np.dot(weights.T, np.dot(covariance, weights))

    penalty = 0
    for weight in weights:
        if weight > 0.5:
            penalty += 1000000
        # if weight < 0:
        #     penalty += 1000000000

    return -(portfolio_return - risk * portfolio_risk) + penalty


def rastrigin_function(weights):
    A = 10
    n = len(weights)
    return A * n + sum((w**2 - A * np.cos(2 * np.pi * w)) for w in weights)


class PSO:
    def __init__(
        self, num_particles, num_assets, returns, covariance, risk=1, iter=100, test=False
    ):
        self.num_particles = num_particles
        self.num_assets = num_assets
        self.returns = returns
        self.covariance = covariance
        self.risk = risk
        self.iter = iter

        self.test = test

        if test:
            self.positions = np.random.uniform(-5.12, 5.12, (num_particles, num_assets))
            self.inertia = 0.9
            self.cognitive = 1.5
            self.social = 1.5
        else:
            # self.positions = np.random.uniform(0, 0.5, (num_particles, num_assets))
            self.positions = np.random.dirichlet(np.ones(num_assets), size=num_particles)
            self.inertia = 0.5
            self.cognitive = 2.0
            self.social = 2.0

        self.velocities = np.random.uniform(-1, 1, (num_particles, num_assets))

        self.personal_best_positions = self.positions.copy()
        self.personal_best_scores = np.array([self.evaluate(p) for p in self.positions])
        self.global_best_position = self.personal_best_positions[
            np.argmin(self.personal_best_scores)
        ]

        self.positions_history = []

    def evaluate(self, weights):
        if self.test:
            return rastrigin_function(weights)
        else:
            return portfolio_objective(weights, self.returns, self.covariance, self.risk)

    def optimize(self):
        for iteration in range(self.iter):
            self.positions_history.append(self.positions.copy())

            for i, position in enumerate(self.positions):
                score = self.evaluate(self.positions[i])

                r1 = np.random.rand()
                r2 = np.random.rand()

                if score < self.personal_best_scores[i]:
                    self.personal_best_scores[i] = score
                    self.personal_best_positions[i] = self.positions[i]

                self.velocities[i] = (
                    self.inertia * self.velocities[i]
                    + self.cognitive * r1 * (self.personal_best_positions[i] - position)
                    + self.social * r2 * (self.global_best_position - position)
                )

                self.positions[i] += self.velocities[i]

                if self.test:
                    self.positions[i] = np.clip(self.positions[i], -5.12, 5.12)
                else:
                    self.positions[i] = np.clip(self.positions[i], 0, 0.5)
                    self.positions[i] /= np.sum(self.positions[i])

            self.global_best_position = self.personal_best_positions[
                np.argmin(self.personal_best_scores)
            ]

        return self.global_best_position

    def plot_positions(self):
        fig, ax = plt.subplots()
        ax.set_title("Particle Swarm Optimization - Particle Positions")

        scatter = ax.scatter([], [], c="blue", label="Particle positions", alpha=0.7)

        ax.set_xlabel("Asset 1 Weight")
        ax.set_ylabel("Asset 2 Weight")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        def update(frame):
            positions_at_frame = self.positions_history[frame]
            scatter.set_offsets(positions_at_frame[:, :2])
            return (scatter,)

        ani = FuncAnimation(
            fig, update, frames=len(self.positions_history), interval=100, blit=True
        )

        ani.save("pso_animation.mp4", writer="ffmpeg", fps=10)
        plt.close(fig)
