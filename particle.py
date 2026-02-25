class Particle:
    def __init__(self, name="", position=None, velocity=None, mass=1.0):
        self.name: str = name
        self.position: list[float] = (
            position.copy() if position is not None else [0.0, 0.0]
        )
        self.previous_position: list = [0.0, 0.0]
        self.previous_acceleration: list = [0.0, 0.0]
        self.velocity: list[float] = (
            velocity.copy() if velocity is not None else [0.0, 0.0]
        )
        self.mass: float = mass
        self.force: list[float] = [0.0, 0.0]
