"""In this module we define the subclass motors, which inherit from the superclass components"""

from components import Component

class Motor(Component):
    def __init__(self, name: str, value: float, types: str, description: str,
                lenght: float, width: float, height: float, torque: float,
                voltageRating: float, current: float, speed: float):
        super().__init__(name, value, types, description, lenght, width, height)
        self.voltageRating = voltageRating
        self.current = current
        self.speed = speed
        self.torque = torque

