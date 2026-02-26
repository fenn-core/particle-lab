import matplotlib.pyplot as plt


class Renderer:
    def render(self, world) -> None:
        raise NotImplementedError


class MatPlotLibRenderer(Renderer):
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        plt.ion()

    def render(self, world) -> None:
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        for particle in world.particles:
            self.ax.scatter(particle.position[0], particle.position[1])

        for constraint in (world.pbd_constraints+world.force_constraints):
            x1: float
            y1: float
            x2: float
            y2: float
            x1 = constraint.anchor1.position[0]
            y1 = constraint.anchor1.position[1]
            x2 = constraint.anchor2.position[0]
            y2 = constraint.anchor2.position[1]
            self.ax.plot([x1, x2], [y1, y2])

        plt.draw()
        plt.pause(0.001)
