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

p1 = sim.Particle(position=[-125, 0])
p1.velocity = np.array([35, 35], dtype="int64")

world.add_particle(p1)

renderer = sim.MatPlotLibRenderer(xlim=[-125, 125], ylim=[0, 75])

world.sim_loop(renderer)
