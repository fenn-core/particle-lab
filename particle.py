import numpy as np
from numpy.typing import NDArray

class Particle:
    def __init__(self, name="", position=None, velocity=None, mass=1.0) -> None:
        self.name: str = name
        self.position: NDArray[np.float64] = (
            np.array(position, dtype="float64") if position is not None else np.zeros(2, dtype="float64")
        )
        self.previous_position: NDArray[np.float64] = self.position.copy()
        self.previous_acceleration: NDArray[np.float64] = np.zeros(2, dtype="float64")
        self.velocity: NDArray[np.float64] = (
            np.array(velocity, dtype="float64") if velocity is not None else np.zeros(2, dtype="float64")
        )
        self.mass: float = mass
        self.force: NDArray[np.float64] = np.zeros(2, dtype="float64")
