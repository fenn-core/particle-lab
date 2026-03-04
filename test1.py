import particle_lab as sim
import numpy as np

world = sim.World(
    integrator=sim.VelocityVerletIntegrator(),
    # dt=0.001,
    sim_time=20,
    FPS=60,
    world_gravity=True,
    particle_gravity=False,
    # G=1,
    eps=0.5,
)

p1 = sim.Particle(position=[-9, -9])
p1.velocity = np.array([6,14], dtype="int64")

world.add_particle(p1)

renderer = sim.MatPlotLibRenderer()

world.sim_loop(renderer)