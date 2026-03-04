import numpy as np
from particle import Particle
from constraint import Constraint
import physics
from integrator import Integrator
from time import time


class World:
    def __init__(
        self,
        integrator: Integrator,
        dt=0.001,
        sim_time=100,
        FPS=60,
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
        self.dt: float = dt
        self.sim_time: float = sim_time
        self.accumulator: float = 0.0
        self.FPS: int = FPS
        self.topology_changed: bool = True
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
        self.topology_changed = True

    def remove_constraint(self, constraint: Constraint) -> None:
        if constraint.applies_force:
            self.force_constraints.remove(constraint)
        else:
            self.pbd_constraints.remove(constraint)
        self.topology_changed = True

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
            particle.force = np.zeros(2, dtype="float64")

    def recompute_velocity(self, dt) -> None:
        for particle in self.particles:
            if particle.mass:
                particle.velocity = (
                    particle.position - particle.previous_position
                ) / dt

    def solve_pbd_constraints(self) -> None:
        for _ in range(self.constraint_iterations):
            for constraint in self.pbd_constraints:
                constraint.solve()

    def step(self, dt) -> None:
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
            elif not (self.integrator.computes_velocity):
                self.recompute_velocity(dt)

        else:
            self.integrator.step(self.particles, dt)
            self.solve_pbd_constraints()
            if self.pbd_constraints:
                self.recompute_velocity(dt)
            elif not (self.integrator.computes_velocity):
                self.recompute_velocity(dt)


    def sim_loop(self, render_engine) -> None:
        dt: float = self.dt
        FPS: int = self.FPS
        sim_time: float = self.sim_time 
        elapsed_time: float = 0
        last_time: float = time()
        frame_time: float = 0
        dt_per_frame: float = 1/FPS
        alpha = 0

        while elapsed_time < sim_time:
            current_time: float = time()
            real_dt: float = current_time - last_time
            last_time = current_time
            self.accumulator += real_dt

            while self.accumulator >= dt:
                self.step(dt)
                self.accumulator -= dt 
                alpha: float = self.accumulator / dt
                elapsed_time += dt
                frame_time += dt

            if frame_time >= dt_per_frame:
                render_engine.render(self, alpha)
                # logger.take_snapshot(world.particles)
                frame_time -= dt_per_frame
