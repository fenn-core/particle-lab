from particle import Particle
from constraint import Constraint
import physics
from integrator import Integrator


class World:
    def __init__(
        self,
        integrator: Integrator,
        world_gravity=True,
        particle_gravity=True,
        G=6.67430e-11,
        eps=1e-5,
        constraint_iterations=10,
    ) -> None:
        self.particles: list[Particle] = []
        self.force_constraints: list[Constraint] = []
        self.pbd_constraints: list[Constraint] = []
        self.constraint_iterations: int = constraint_iterations
        self.integrator: Integrator = integrator
        self.world_gravity: bool = world_gravity
        self.particle_gravity: bool = particle_gravity
        self.G: float = G
        self.eps: float = eps

    def add_particle(self, particle: Particle) -> None:
        self.particles.append(particle)

    def remove_particle(self, particle: Particle) -> None:
        self.particles.remove(particle)

    def add_constraint(self, constraint: Constraint) -> None:
        if constraint.applies_force:
            self.force_constraints.append(constraint)
        else:
            self.pbd_constraints.append(constraint)

    def remove_constraint(self, constraint: Constraint) -> None:
        if constraint.applies_force:
            self.force_constraints.remove(constraint)
        else:
            self.pbd_constraints.remove(constraint)

    def apply_forces(self) -> None:
        particles_amount: int = len(self.particles)
        if self.world_gravity:
            for particle in self.particles:
                physics.global_gravity(particle)
        if self.particle_gravity:
            for i in range(particles_amount - 1):
                for j in range(i + 1, particles_amount):
                    physics.apply_gravitational_force(
                        self.particles[i], self.particles[j], self.G, self.eps
                    )
        for constraint in self.force_constraints:
            constraint.solve()

    def reset_forces(self) -> None:
        for particle in self.particles:
            particle.force = [0.0, 0.0]

    def recompute_velocity(self, dt) -> None:
        for particle in self.particles:
            if particle.mass:   
                particle.velocity[0] = (
                    particle.position[0] - particle.previous_position[0]
                ) / dt
                particle.velocity[1] = (
                    particle.position[1] - particle.previous_position[1]
                ) / dt
    
    def solve_pbd_constraints(self) -> None:
        for _ in range(self.constraint_iterations):
            for constraint in self.pbd_constraints:
                constraint.solve()
        
    def step(self, dt=0.01) -> None:
        self.reset_forces()
        self.apply_forces()
        if self.integrator.multi_step:
            self.integrator.position_step(self.particles, dt)
            self.reset_forces()
            self.apply_forces()
            self.integrator.velocity_step(self.particles, dt)
            self.solve_pbd_constraints()
            if self.pbd_constraints:
                self.recompute_velocity(dt)
            elif not(self.integrator.computes_velocity):    
                self.recompute_velocity(dt)

        else:
            self.integrator.step(self.particles, dt)
            self.solve_pbd_constraints()
            if self.pbd_constraints:
                self.recompute_velocity(dt)
            elif not(self.integrator.computes_velocity):    
                self.recompute_velocity(dt)
                