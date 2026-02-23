class Integrator:
    def step(self, particles, dt):
        raise NotImplementedError


class EulerIntegrator(Integrator):
    def step(self, particles, dt):
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