from world import World 
from integrator import EulerIntegrator, VerletIntegrator
from particle import Particle
import renderer
import constraint

world = World(integrator=VerletIntegrator(), world_gravity=False, particle_gravity=True, G=1)
p1 = Particle(position=[0, 5], mass=10)
p2 = Particle(position=[0, 0], mass=500)

p1.velocity = [10,0]

world.add_particle(p1)
world.add_particle(p2)


renderer = renderer.MatPlotLibRenderer()

while True:
    world.step(dt=0.01)
    renderer.render(world)