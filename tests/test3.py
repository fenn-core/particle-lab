import particle_lab as sim

world = sim.World(
    integrator=sim.VelocityVerletIntegrator(),
    dt=0.001,
    sim_time=20000,
    FPS=60,
    world_gravity=True  ,
    particle_gravity=False,
    # G=1
    eps=0.5,
)
p1 = sim.Particle(position=[0, 8], mass=0)
p2 = sim.Particle(position=[3, 5], mass=40)
p3 = sim.Particle(position=[7, 1], mass=40)
p4 = sim.Particle(position=[10, -3], mass=40)

c1 = sim.Rod(5, p1, p2)
c2 = sim.Rod(5, p2, p3)
c3 = sim.Rod(5, p3, p4)

world.add_particle(p1)
world.add_particle(p2)
world.add_particle(p3)
world.add_particle(p4)
world.add_constraint(c1)
world.add_constraint(c2)
world.add_constraint(c3)

renderer = sim.MatPlotLibRenderer(xlim=(-10,10), ylim=(-10,10))

world.sim_loop(renderer)