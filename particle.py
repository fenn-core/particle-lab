class Particle:
    def __init__(self, name=None, position=None, velocity=None, mass=1.0):
        self.name = name
        self.position = position.copy() if position is not None else [0.0, 0.0]
        self.previous_position = None
        self.previous_acceleration = None
        self.velocity = velocity.copy() if velocity is not None else [0.0, 0.0]
        self.mass = mass
        self.force = [0.0, 0.0]