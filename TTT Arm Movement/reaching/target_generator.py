import random


class TargetGenerator:
    """
    Generates random 3D reaching targets.

    All positions are measured in metres.

    Coordinates must be expressed in the same
    reference frame as the robot's hand position.
    """

    def __init__(
        self,
        x_range=(0.30, 0.60),
        y_range=(-0.35, -0.10),
        z_range=(0.75, 0.95),
        seed=None
    ):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

        # Independent random generator
        self.rng = random.Random(seed)

    def generate_target(self):
        """
        Generate one random target position.
        """

        x = self.rng.uniform(*self.x_range)
        y = self.rng.uniform(*self.y_range)
        z = self.rng.uniform(*self.z_range)

        return [x, y, z]

    def generate_batch(self, count):
        """
        Generate multiple target positions.
        """

        return [
            self.generate_target()
            for _ in range(count)
        ]