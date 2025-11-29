""" In this module we define the subclass capacitors,
which inherit from the superclass components"""

from components import Component

class Capacitor(Component):
    def __init__(self, name: str, value: float, types: str,
                lenght: float, width: float, height: float,
                voltageRating: float, description: str):
        super().__init__(name, value, types, lenght, width, height, description)
        self.voltageRating = voltageRating
    
    def breakdown(self, operationVoltage: float) -> str:
        if operationVoltage > self.voltageRating:
            return f"The capacitor {self.name} has broken down!"
        else:
            return f"The capacitor {self.name} is operating within safe limits."
        
