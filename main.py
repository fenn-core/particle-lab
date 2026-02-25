from world import World 
import integrator
from particle import Particle
import renderer
import constraint

world = World(integrator=integrator.VelocityVerletIntegrator(), 
              world_gravity=False, particle_gravity=True, G=1, eps=0.5)
p1 = Particle(position=[0, 5], mass=100)
p2 = Particle(position=[0, 0], mass=500)
p3 = Particle(position=[-5,-7], mass=250)

world.add_particle(p1)
world.add_particle(p2)
world.add_particle(p3)

renderer = renderer.MatPlotLibRenderer()

while True:
    world.step(dt=0.01)
    renderer.render(world)