from particle import Particle
from constraint import Constraint
import physics
from integrator import Integrator

class World:
    def __init__(self, integrator:Integrator, world_gravity=True, 
                 particle_gravity=True, G = 6.67430e-11,
                 eps=1e-5, constraint_iterations=10
                 ) -> None:
        self.particles = []
        self.constraints = []
        self.constraint_iterations = constraint_iterations
        self.integrator = integrator
        self.world_gravity = world_gravity
        self.particle_gravity = particle_gravity
        self.G = G
        self.eps = eps

    def add_particle(self, particle:Particle) -> None:
        self.particles.append(particle)
    
    def remove_particle(self, particle:Particle) -> None:
        self.particles.remove(particle)

    def add_constraint(self, constraint:Constraint) -> None:
        self.constraints.append(constraint)

    def remove_constraint(self, constraint:Constraint) -> None:
        self.constraints.remove(constraint)

    def apply_forces(self) -> None:
        particles_amount = len(self.particles)
        if self.world_gravity:
            for particle in self.particles:
                physics.global_gravity(particle)
        if self.particle_gravity:
            for i in range(particles_amount-1):
                for j in range(i+1, particles_amount):
                    physics.apply_gravitational_force(
                        self.particles[i], self.particles[j], self.G, self.eps) 

    def step(self, dt=0.01) -> None:
        self.apply_forces()

        if self.integrator.multi_step:
            self.integrator.position_step(self.particles, dt)
            for particle in self.particles:
                particle.force = [0.0, 0.0]
            self.apply_forces()
            self.integrator.velocity_step(self.particles, dt)
        else: 
            self.integrator.step(self.particles, dt)

        for _ in range(self.constraint_iterations):
            for constraint in self.constraints:
                constraint.solve()
        for particle in self.particles:
            if particle.mass == 0:
                continue

            if not(self.integrator.updates_velocity):
                particle.velocity[0] = (
                    (particle.position[0] - particle.previous_position[0]) / dt)
                particle.velocity[1] = (
                    (particle.position[1] - particle.previous_position[1]) / dt)
            
        for particle in self.particles:
            particle.force = [0.0, 0.0]
