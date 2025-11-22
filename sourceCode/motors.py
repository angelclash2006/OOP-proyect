"""In this module, we define various motor classes for different types of motors. And their main types"""
from components import Component

class Motor(Component):
    """Base class for all motors."""
    def __init__(self, name: str, description: str, pieceNumber: str, dimensions: dict):
        super().__init__(name, description, pieceNumber, parameters={}, dimensions={})
        self.speed = 0  # Speed of the motor
        self.torque = 0  # Torque of the motor

    def set_speed(self, speed):
        """Set the speed of the motor."""
        self.speed = speed

    def get_speed(self):
        """Get the current speed of the motor."""
        return self.speed