from math import sqrt


def compute_deltas(position1, position2) -> tuple:
    dx: float
    dy: float
    dx = position2[0] - position1[0]
    dy = position2[1] - position1[1]
    return dx, dy


def compute_distance(position1, position2) -> float:
    dx: float
    dy: float
    dx, dy = compute_deltas(position1, position2)
    return sqrt(dx * dx + dy * dy)
