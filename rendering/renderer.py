import matplotlib.pyplot as plt
from particle_lab.utils.utils import lerp
import numpy as np
from numpy.typing import NDArray

class Renderer:
    def render(self, world, alpha) -> None:
        raise NotImplementedError
    

class MatPlotLibRenderer(Renderer):
    def __init__(self, xlim=(-10, 10), ylim=(-10, 10)) -> None:
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.xlim: tuple[float, float] = xlim
        self.ylim: tuple[float, float] = ylim
        self.ax.set_xlim(self.xlim[0], self.xlim[1])
        self.ax.set_ylim(self.ylim[0], self.ylim[1])
        self.particle_scatter = self.ax.scatter([], [])
        self.constraint_lines: list = []
        plt.ion()

    def sync_world(self, world) -> None:
        for line in self.constraint_lines:
            line.remove()
        self.all_constraints: list = (world.pbd_constraints 
                                    + world.force_constraints)
        self.constraint_lines = [
        self.ax.plot([], [])[0]
        for _ in world.pbd_constraints + world.force_constraints
        ]

    def render(self, world, alpha) -> None:
        if world.topology_changed:
            self.sync_world(world)
            world.topology_changed = False
            
        positions: NDArray = np.array([
            lerp(p.previous_position, p.position, alpha) 
            for p in world.particles 
        ])
        self.particle_scatter.set_offsets(positions)
        for line, constraint in zip(self.constraint_lines, self.all_constraints):
            x1, y1 = lerp(constraint.anchor1.previous_position,
                                    constraint.anchor1.position,
                                    alpha)
            x2, y2 = lerp(constraint.anchor2.previous_position,
                                    constraint.anchor2.position,
                                    alpha)
            line.set_data([x1, x2], [y1, y2])
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        plt.show()
