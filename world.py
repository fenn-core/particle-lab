from particle import Particle 
import physics

class World:
    def __init__(self, integrator, world_gravity=True, 
                 particle_gravity=True, G = 6.67430e-11,
                 eps=1e-5
                 ):
        self.particles = []
        self.constraints = []
        self.constraint_iterations = 10
        self.integrator = integrator
        self.world_gravity = world_gravity
        self.particle_gravity = particle_gravity
        self.G = G
        self.eps = eps

    def add_particle(self, particle):
        self.particles.append(particle)
    
    def remove_particle(self, particle):
        self.particles.remove(particle)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def remove_constraint(self, constraint):
        self.constraints.remove(constraint)

    def step(self, dt=0.01):
        particles_amount = len(self.particles)
        if self.world_gravity:
            for particle in self.particles:
                physics.global_gravity(particle)
        if self.particle_gravity:
            for i in range(particles_amount-1):
                for j in range(i+1, particles_amount):
                    physics.apply_gravitational_force(
                        self.particles[i], self.particles[j], self.G, self.eps)
                    
        self.integrator.step(self.particles, dt)

        for _ in range(self.constraint_iterations):
            for constraint in self.constraints:
                constraint.solve()
        for particle in self.particles:
            if particle.mass == 0:
                continue
            particle.velocity[0] = (
                (particle.position[0] - particle.previous_position[0]) / dt)
            particle.velocity[1] = (
                (particle.position[1] - particle.previous_position[1]) / dt)
            
        for particle in self.particles:
            particle.force = [0.0, 0.0]

