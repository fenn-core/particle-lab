class Integrator:
    multi_step: bool = False
    updates_velocity: bool = False

    def step(self, particles: list, dt: float):
        raise NotImplementedError


class EulerIntegrator(Integrator):
    def __init__(self) -> None:
        self.multi_step = False
        self.updates_velocity = False

    def step(self, particles: list, dt: float) -> None:
        for particle in particles:
            if particle.mass == 0:
                continue
            a_x = particle.force[0] / particle.mass
            a_y = particle.force[1] / particle.mass
            particle.velocity[0] += a_x * dt
            particle.velocity[1] += a_y * dt
            particle.previous_position = particle.position.copy()
            particle.position[0] += particle.velocity[0] * dt
            particle.position[1] += particle.velocity[1] * dt


class VerletIntegrator(Integrator):
    def __init__(self) -> None:
        self.multi_step = False
        self.updates_velocity = False

    def step(self, particles: list, dt: float, d=0.001) -> None:
        for particle in particles:
            if particle.mass == 0:
                continue
            a_x = particle.force[0] / particle.mass
            a_y = particle.force[1] / particle.mass
            if particle.previous_position is None:
                particle.previous_position = [
                    (particle.position[0] - particle.velocity[0] * dt),
                    (particle.position[1] - particle.velocity[1] * dt),
                ]

            temp = particle.position.copy()
            particle.position[0] = (
                particle.position[0]
                + (particle.position[0] - particle.previous_position[0]) * (1 - d)
                + a_x * dt * dt
            )
            particle.position[1] = (
                particle.position[1]
                + (particle.position[1] - particle.previous_position[1]) * (1 - d)
                + a_y * dt * dt
            )
            particle.previous_position = temp


class VelocityVerletIntegrator(Integrator):
    def __init__(self) -> None:
        self.multi_step = True
        self.updates_velocity = True

    def position_step(self, particles: list, dt: float) -> None:
        for particle in particles:
            if particle.mass == 0:
                continue
            a_x = particle.force[0] / particle.mass
            a_y = particle.force[1] / particle.mass
            particle.previous_acceleration = [a_x, a_y]
            particle.position[0] = (
                particle.position[0] + particle.velocity[0] * dt + 0.5 * a_x * dt * dt
            )
            particle.position[1] = (
                particle.position[1] + particle.velocity[1] * dt + 0.5 * a_y * dt * dt
            )

    def velocity_step(self, particles: list, dt: float) -> None:
        for particle in particles:
            if particle.mass == 0:
                continue
            if particle.previous_acceleration is None:
                particle.previous_acceleration = [0.0, 0.0]
            a_x1, a_y1 = particle.previous_acceleration
            a_x = particle.force[0] / particle.mass
            a_y = particle.force[1] / particle.mass
            particle.velocity[0] = particle.velocity[0] + 0.5 * (a_x + a_x1) * dt
            particle.velocity[1] = particle.velocity[1] + 0.5 * (a_y + a_y1) * dt
