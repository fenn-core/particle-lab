from numpy.typing import NDArray
from numpy import zeros


class Integrator:
    multi_step: bool = False
    computes_velocity: bool = False

    def step(self, particles: list, dt: float) -> None:
        raise NotImplementedError

    def position_step(self, particles: list, dt: float) -> None:
        raise NotImplementedError

    def velocity_step(self, particles: list, dt: float) -> None:
        raise NotImplementedError


class EulerIntegrator(Integrator):
    def __init__(self) -> None:
        self.multi_step: bool = False
        self.computes_velocity: bool = True

    def step(self, particles: list, dt: float) -> None:
        for particle in particles:
            if particle.mass == 0:
                continue
            acceleration: NDArray = particle.force / particle.mass
            particle.velocity += acceleration * dt
            particle.previous_position = particle.position.copy()
            particle.position += particle.velocity * dt


class VerletIntegrator(Integrator):
    def __init__(self) -> None:
        self.multi_step = False
        self.computes_velocity: bool = False

    def step(self, particles: list, dt: float, d=0.001) -> None:
        for particle in particles:
            if particle.mass == 0:
                continue
            acceleration: NDArray = particle.force / particle.mass
            if particle.previous_position is None:
                particle.previous_position = (particle.position - particle.velocity * dt)
                
            temp: NDArray = particle.position.copy()
            particle.position = (
                particle.position
                + (particle.position - particle.previous_position) * (1 - d)
                + acceleration * dt * dt
            )
            particle.previous_position = temp


class VelocityVerletIntegrator(Integrator):
    def __init__(self) -> None:
        self.multi_step: bool = True
        self.computes_velocity: bool = True

    def position_step(self, particles: list, dt: float) -> None:
        for particle in particles:
            if particle.mass == 0:
                continue
            acceleration: NDArray = particle.force / particle.mass
            particle.previous_acceleration = acceleration.copy()
            particle.previous_position = particle.position.copy()
            particle.position = (
                particle.position + particle.velocity * dt + 0.5 * acceleration * dt * dt
            )
            
    def velocity_step(self, particles: list, dt: float) -> None:
        for particle in particles:
            if particle.mass == 0:
                continue
            if particle.previous_acceleration is None:
                particle.previous_acceleration = zeros(2, dtype="float64")
            acceleration: NDArray = particle.force / particle.mass
            particle.velocity = particle.velocity + 0.5 * (acceleration + particle.previous_acceleration) * dt
