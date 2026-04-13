from particle_lab.physics.particle import Particle
from particle_lab.physics.constraint import Constraint
import numpy as np
from numpy.typing import NDArray


class Frame:
    def __init__(
        self,
        time,
        particles: list[Particle],
        force_constraints: list[Constraint],
        pbd_constraints: list[Constraint],
    ) -> None:
        self.time: float = time
        self.particle_count: int = len(particles)
        self.particle_positions: NDArray = np.zeros(
            (self.particle_count, 2), dtype="float64"
        )
        self.particle_ids: NDArray = np.zeros(self.particle_count, dtype="int")
        for idx, particle in enumerate(particles):
            self.particle_positions[idx] = particle.position
            self.particle_ids[idx] = particle.particle_id

        self.constraint_relationships: list[tuple] = []
        for constraint in force_constraints + pbd_constraints:
            self.constraint_relationships.append(
                (
                    constraint.anchor1.particle_id,
                    constraint.anchor2.particle_id,
                    constraint.constraint_type,
                )
            )
