from particle_lab.physics.particle import Particle
import numpy as np
from numpy.typing import NDArray

class DataLogger:
    def __init__(self, log_indices=None) -> None:
        self.log_indices: list[int] | None = log_indices
        
    def take_snapshot(
        self,
        global_particles,
        log_indices,
        log_position=True,
        log_velocity=True,
        log_acceleration=True,
        log_energy=True                                      
) -> None:
        if log_indices is not None:
            self.particles: list[Particle] = list()
            for idx in log_indices:
                self.particles.append(global_particles[idx])
        else:
            self.particles = global_particles.copy()
        
        if log_position:
            pass
        if log_velocity:
            pass
        if log_acceleration:
            pass
        if log_energy:
            pass

        snapshot: dict[str, NDArray] = {
            "position" : np.array(),
            "velocity" : np.array(),
            "acceleration" : np.array(),
            "potential_energy" : np.array(),
            "kinetic_energy" : np.array()
        }