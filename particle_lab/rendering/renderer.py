import matplotlib.pyplot as plt
from particle_lab.utils.utils import lerp
from numpy.typing import NDArray


class Renderer:
    def render(self, previous_frame, current_frame, alpha) -> None:
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

    def sync_constraints(self, frame) -> None:
        for line in self.constraint_lines:
            line.remove()
        self.constraint_lines = [
            self.ax.plot([], [])[0] for _ in frame.constraint_relationships
        ]

    def render(self, previous_frame, current_frame, alpha) -> None:
        if len(self.constraint_lines) != len(current_frame.constraint_relationships):
            self.sync_constraints(current_frame)

        positions: NDArray = lerp(
            previous_frame.particle_positions,
            current_frame.particle_positions,
            alpha,
        )

        self.particle_scatter.set_offsets(positions)
        for line, constraint_data in zip(
            self.constraint_lines,
            current_frame.constraint_relationships,
        ):

            p1_index: int = constraint_data[0]
            p2_index: int = constraint_data[1]

            x1, y1 = (
                positions[p1_index][0],
                positions[p1_index][1],
            )

            x2, y2 = (
                positions[p2_index][0],
                positions[p2_index][1],
            )

            line.set_data([x1, x2], [y1, y2])
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        plt.show()
