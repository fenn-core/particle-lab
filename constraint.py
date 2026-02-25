import utils
import physics
from particle import Particle


class Constraint:
    def solve(self):
        raise NotImplementedError


class Rod(Constraint):
    def __init__(
        self, length: float, anchor1: Particle, anchor2: Particle, stiffness=1.0
    ) -> None:
        self.anchor1 = anchor1
        self.anchor2 = anchor2
        self.length = length
        self.stiffness = stiffness
        self.applies_forces = False

    # implementation is positional for now, velocity based correction is planned
    def compute_constraint(self) -> None:
        distance = utils.compute_distance(self.anchor1.position, self.anchor2.position)
        if distance == 0:
            return 0, 0, 0, 0
        error = (distance - self.length) * self.stiffness
        dx, dy = utils.compute_deltas(self.anchor1.position, self.anchor2.position)
        direction_x = dx / distance
        direction_y = dy / distance
        w1 = 0 if self.anchor1.mass == 0 else 1 / self.anchor1.mass
        w2 = 0 if self.anchor2.mass == 0 else 1 / self.anchor2.mass
        w_sum = w1 + w2
        if w_sum == 0:
            return 0, 0, 0, 0

        return (
            direction_x * error * (w1 / w_sum),
            direction_y * error * (w1 / w_sum),
            direction_x * error * (w2 / w_sum),
            direction_y * error * (w2 / w_sum),
        )

    def solve(self) -> None:
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
        self.anchor1 = anchor1
        self.anchor2 = anchor2
        self.length = length
        self.spring_constant = spring_constant
        self.damping_constant = damping_constant
        self.applies_force = True

    def compute_constraint(self) -> tuple:
        distance = utils.compute_distance(self.anchor1.position, self.anchor2.position)
        if distance == 0:
            return 0, 0
        dx, dy = utils.compute_deltas(self.anchor1.position, self.anchor2.position)
        direction_x = dx / distance
        direction_y = dy / distance
        extension = distance - self.length
        spring_force = self.spring_constant * extension
        if self.damping_constant != 0.0:
            relative_velocity_x = self.anchor2.velocity[0] - self.anchor1.velocity[0]
            relative_velocity_y = self.anchor2.velocity[1] - self.anchor1.velocity[1]
            relative_velocity = (
                relative_velocity_x * direction_x + relative_velocity_y * direction_y
            )
            damping_force = -self.damping_constant * relative_velocity
        else:
            damping_force = 0.0

        force = spring_force - damping_force
        force_x = force * direction_x
        force_y = force * direction_y

        return force_x, force_y

    def solve(self) -> None:
        force_x, force_y = self.compute_constraint()
        if self.anchor1.mass != 0:
            physics.apply_force(self.anchor1, force_x, force_y)
        if self.anchor2.mass != 0:
            physics.apply_force(self.anchor2, -force_x, -force_y)
