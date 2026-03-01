from world import World
import integrator
from particle import Particle
import renderer
import constraint

world = World(
    integrator=integrator.VelocityVerletIntegrator(),
    world_gravity=True,
    particle_gravity=False,
    # G=1,
    eps=0.5,
)
p1 = Particle(position=[0, 8], mass=0)
p2 = Particle(position=[0, 0], mass=5)
p3 = Particle(position=[2, 8], mass=0)
p4 = Particle(position=[2, -2], mass=5)

c1 = constraint.Spring(5.0, p1, p2, 1000, damping_constant=2)
c2 = constraint.Spring(5.0, p3, p4, 1000, damping_constant=2)


world.add_particle(p1)
world.add_particle(p2)
world.add_particle(p3)
world.add_particle(p4)
world.add_constraint(c1)
world.add_constraint(c2)

renderer = renderer.MatPlotLibRenderer()

while True:

    world.step(dt=0.01)
    renderer.render(world)
