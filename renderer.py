import matplotlib.pyplot as plt
from particle import Particle
from utils import lerp

class Renderer:
    def render(self, world, alpha) -> None:
        raise NotImplementedError
    

class MatPlotLibRenderer(Renderer):
    def __init__(self, xlim=(-10, 10), ylim=(-10, 10)) -> None:
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.xlim: tuple[float, float] = xlim
        self.ylim: tuple[float, float] = ylim
        plt.ion()

    def render(self, world, alpha) -> None:
        self.ax.clear()
        self.ax.set_xlim(self.xlim[0], self.xlim[1])
        self.ax.set_ylim(self.ylim[0], self.ylim[1])
        for particle in world.particles:
            render_x, render_y  = lerp(particle.previous_position,
                                               particle.position,
                                               alpha)
            self.ax.scatter(render_x, render_y)

        for constraint in world.pbd_constraints + world.force_constraints:
            p1: Particle = constraint.anchor1
            p2: Particle = constraint.anchor2
            x1, y1 = lerp(p1.previous_position, p1.position, alpha)
            x2, y2 = lerp(p2.previous_position, p2.position, alpha)
            self.ax.plot([x1, x2], [y1, y2])

        plt.draw()
        plt.pause(0.001)
