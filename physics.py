import utils
from math import sqrt 

def apply_force(particle, magnitude_x, magnitude_y):
    particle.force[0] += magnitude_x
    particle.force[1] += magnitude_y

def global_gravity(particle, a_y=-9.80665):
    force = a_y * particle.mass
    apply_force(particle, 0, force)

# class Drag:
# drag class will replace the function soon

def apply_drag(particle, k=0.1): 
    apply_force(particle, 
                -particle.velocity[0]*k, 
                -particle.velocity[1]*k)

def apply_gravitational_force(particle1, particle2, G = 6.67430e-11, eps=1e-5):
    
    dx, dy = utils.compute_deltas(particle1.position ,particle2.position)
    r2 = dx*dx + dy*dy + eps*eps 
    inv_r = 1 / sqrt(r2)
    inv_r3 = inv_r / r2 

    force_x = -G * particle1.mass * particle2.mass * dx * inv_r3
    force_y = -G * particle1.mass * particle2.mass * dy * inv_r3

    apply_force(particle1, force_x, force_y)
    apply_force(particle2, -force_x, -force_y)
