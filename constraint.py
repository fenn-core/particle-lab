from typing import Literal

import utils
import physics
from particle import Particle


class Constraint:
    applies_force: bool

    def solve(self) -> None:
        raise NotImplementedError


class Rod(Constraint):
    def __init__(
        self, length: float, anchor1: Particle, anchor2: Particle, stiffness=1.0
    ) -> None:
        self.anchor1: Particle = anchor1
        self.anchor2: Particle = anchor2
        self.length: float = length
        self.stiffness: float = stiffness
        self.applies_force: bool = False

    # implementation is positional for now, velocity based correction is planned
    def compute_constraint(self) -> tuple:
        distance: float = utils.compute_distance(
            self.anchor1.position, self.anchor2.position
        )
        if distance == 0:
            return 0, 0, 0, 0
        error: float = (distance - self.length) * self.stiffness
        dx: float
        dy: float
        dx, dy = utils.compute_deltas(self.anchor1.position, self.anchor2.position)
        direction_x: float = dx / distance
        direction_y: float = dy / distance
        w1: float | Literal[0] = 0 if self.anchor1.mass == 0 else 1 / self.anchor1.mass
        w2: float | Literal[0] = 0 if self.anchor2.mass == 0 else 1 / self.anchor2.mass
        w_sum: float | int = w1 + w2
        if w_sum == 0:
            return 0, 0, 0, 0

        return (
            direction_x * error * (w1 / w_sum),
            direction_y * error * (w1 / w_sum),
            direction_x * error * (w2 / w_sum),
            direction_y * error * (w2 / w_sum),
        )

    def solve(self) -> None:
        p1_x_cor: float
        p1_y_cor: float
        p2_x_cor: float
        p2_y_cor: float
        p1_x_cor, p1_y_cor, p2_x_cor, p2_y_cor = self.compute_constraint()
        self.anchor1.position[0] += p1_x_cor
        self.anchor1.position[1] += p1_y_cor
        self.anchor2.position[0] -= p2_x_cor
        self.anchor2.position[1] -= p2_y_cor


class Spring(Constraint):
    def __init__(
        self,
        length: float,
        anchor1: Particle,
        anchor2: Particle,
        spring_constant: float,
        damping_constant=0.0,
    ) -> None:
        self.anchor1: Particle = anchor1
        self.anchor2: Particle = anchor2
        self.length: float = length
        self.spring_constant: float = spring_constant
        self.damping_constant: float = damping_constant
        self.applies_force: bool = True

    def compute_constraint(self) -> tuple:
        distance: float = utils.compute_distance(
            self.anchor1.position, self.anchor2.position
        )
        if distance == 0:
            return 0, 0
        dx: float
        dy: float
        dx, dy = utils.compute_deltas(self.anchor1.position, self.anchor2.position)
        direction_x: float = dx / distance
        direction_y: float = dy / distance
        extension: float = distance - self.length
        spring_force: float = self.spring_constant * extension
        if self.damping_constant != 0.0:
            relative_velocity_x: float = (
                self.anchor2.velocity[0] - self.anchor1.velocity[0]
            )
            relative_velocity_y: float = (
                self.anchor2.velocity[1] - self.anchor1.velocity[1]
            )
            relative_velocity: float = (
                relative_velocity_x * direction_x + relative_velocity_y * direction_y
            )
            damping_force: float = -self.damping_constant * relative_velocity
        else:
            damping_force = 0.0

        force: float = spring_force - damping_force
        force_x: float = force * direction_x
        force_y: float = force * direction_y

        return force_x, force_y

    def solve(self) -> None:
        force_x: float
        force_y: float
        force_x, force_y = self.compute_constraint()
        if self.anchor1.mass != 0:
            physics.apply_force(self.anchor1, force_x, force_y)
        if self.anchor2.mass != 0:
            physics.apply_force(self.anchor2, -force_x, -force_y)
