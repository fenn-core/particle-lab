from math import hypot


def compute_deltas(position1, position2) -> tuple:
    return position2 - position1


def compute_distance(position1, position2) -> float:
    dx: float
    dy: float
    dx, dy = compute_deltas(position1, position2)
    return hypot(dx, dy)
