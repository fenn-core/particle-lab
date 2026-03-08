from math import hypot
from numpy.typing import NDArray

def compute_deltas(position1: NDArray, position2: NDArray) -> NDArray:
        return position2 - position1


def compute_distance(position1: NDArray, position2: NDArray) -> float:
    dx: float
    dy: float
    dx, dy = compute_deltas(position1, position2)
    return hypot(dx, dy)

def lerp(x1: NDArray, x2: NDArray, alpha: float) -> NDArray:
    if 0 <= alpha and alpha < 1:
        return (x1 * (1 - alpha) + x2 * alpha)
    return x2
