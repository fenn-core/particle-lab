import particle_lab as sim

world = sim.World(
    integrator=sim.VelocityVerletIntegrator(),
    # dt=0.001,
    sim_time=30,
    FPS=60,
    world_gravity=False,
    particle_gravity=True,
    G=1,
    eps=0.5,
)

p1 = sim.Particle(position=[-7, -9], mass=1000)
p2 = sim.Particle(position=[2, 7], mass=1000)
p3 = sim.Particle(position=[7, -4], mass=1000)

world.add_particle(p1)
world.add_particle(p2)
world.add_particle(p3)

renderer = sim.MatPlotLibRenderer()

world.sim_loop(renderer)