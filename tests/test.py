import particle_lab as sim

world = sim.World(
    integrator=sim.VelocityVerletIntegrator(),
    dt=0.001,
    sim_time=20000,
    FPS=60,
    world_gravity=True,
    particle_gravity=False,
    # G=1
    eps=0.5,
)
p1 = sim.Particle(position=[0, 8], mass=0)
p2 = sim.Particle(position=[0, 0], mass=40)
p3 = sim.Particle(position=[2, 8], mass=0)
p4 = sim.Particle(position=[2, -2], mass=40)
p5 = sim.Particle(position=[2, -6], mass=40)

c1 = sim.Spring(5.0, p1, p2, 1000, damping_constant=2)
c2 = sim.Spring(5.0, p3, p4, 1000, damping_constant=2)
c3 = sim.Spring(5.0, p4, p5, 1000, damping_constant=2)


world.add_particle(p1)
world.add_particle(p2)
world.add_particle(p3)
world.add_particle(p4)
world.add_particle(p5)
world.add_constraint(c1)
world.add_constraint(c2)
world.add_constraint(c3)

renderer = sim.MatPlotLibRenderer(xlim=(-3, 6), ylim=(-15, 9))

world.sim_loop(renderer)