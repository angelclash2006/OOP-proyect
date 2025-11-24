""" In this module we define the subclass capacitors,
which inherit from the superclass components"""

from components import Component

class Capacitor(Component):
    def __init__(self, name: str, value: float, types: str,
                lenght: float, width: float, height: float,
                voltageRating: float, description: str):
        super().__init__(name, value, types, lenght, width, height, description)
        self.voltageRating = voltageRating
    
