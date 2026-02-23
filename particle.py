class Particle:
    def __init__(self, position=[0.0, 0.0], velocity=[0.0, 0.0], mass=1.0):
        self.position = position
        self.previous_position = position.copy()
        self.velocity = velocity
        self.mass = mass
        self.force = [0.0, 0.0]