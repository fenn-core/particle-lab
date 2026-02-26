import utils
from math import sqrt
from particle import Particle


def apply_force(particle: Particle, magnitude_x: float, magnitude_y: float) -> None:
    particle.force[0] += magnitude_x
    particle.force[1] += magnitude_y


def global_gravity(particle: Particle, a_y=-9.80665) -> None:
    if particle.mass != 0:
        force: float = a_y * particle.mass
        apply_force(particle, 0, force)


# class Drag:
# drag class will replace the function soon


def apply_drag(particle: Particle, k=0.1) -> None:
    apply_force(particle, -particle.velocity[0] * k, -particle.velocity[1] * k)


def apply_gravitational_force(
    particle1: Particle, particle2: Particle, G: float, eps: float
) -> None:

    dx: float
    dy: float
    r2: float
    inv_r: float
    inv_r3: float

    dx, dy = utils.compute_deltas(particle1.position, particle2.position)
    r2 = dx * dx + dy * dy + eps * eps
    inv_r = 1 / sqrt(r2)
    inv_r3 = inv_r / r2

    force_x: float = G * particle1.mass * particle2.mass * dx * inv_r3
    force_y: float = G * particle1.mass * particle2.mass * dy * inv_r3

    apply_force(particle1, force_x, force_y)
    apply_force(particle2, -force_x, -force_y)
