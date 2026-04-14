from particle_lab.core.world import World
from particle_lab.core.frame import Frame
import pandas as pd
from numpy.typing import NDArray


class FrameLogger:
    def __init__(self, world: World) -> None:
        self.world: World = world

    def acquire_data(self, world: World) -> None:
        frames: list[Frame] = world.frames
        particle_ids: NDArray = frames[0].particle_ids

        for particle_id in particle_ids:
            particle_data: dict = {
                "time": [],
                "x": [],
                "y": [],
            }
            for frame in frames:
                


    def export_frames_to_csv(self, world: World) -> None:
        self.acquire_data(world)

    def print_frame_data(self, world: World) -> None:
        self.acquire_data(world)
