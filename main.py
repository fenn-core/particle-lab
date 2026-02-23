from world import World 
from integrator import EulerIntegrator
from particle import Particle
import renderer
import constraint

world = World(integrator=EulerIntegrator(), world_gravity=False, 
              particle_gravity=True, G=1, eps=1)

p1 = Particle(position=[0,0], mass=1000)
p2 = Particle(position=[3,0], mass=1000)
p3 = Particle(position=[0,4], mass=1000)
p4 = Particle(position=[10,10], mass=1000)

rod1 = constraint.Rod(5, p1, p2) 
world.add_particle(p1)
world.add_particle(p2)
world.add_particle(p3)
world.add_particle(p4)
world.add_constraint(rod1)

renderer = renderer.MatPlotLibRenderer()

while True:
    world.step(dt=0.01)
    renderer.render(world)