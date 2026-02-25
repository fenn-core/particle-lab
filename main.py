from world import World 
import integrator
from particle import Particle
import renderer
import constraint

world = World(integrator=integrator.VelocityVerletIntegrator(), 
              world_gravity=True, particle_gravity=False)
p1 = Particle(position=[0,8], mass=0)
p2 = Particle(position=[0, 3], mass=1)

spring = constraint.Spring(length= 4,
                           anchor1=p1, anchor2=p2,
                           spring_constant=10000)

world.add_particle(p1)
world.add_particle(p2)
world.add_constraint(spring)

renderer = renderer.MatPlotLibRenderer()

while True:
    world.step(dt=0.01)
    print(p2.force[0])
    renderer.render(world)
    print(p2.velocity[1])