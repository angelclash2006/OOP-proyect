"""In this module, are defined the subclass resistors, which inherit from the superclass components.
also incudes the own atributtes and methods of resistors."""

from components import Component

class Resistor(Component):
    def __init__(self, name: str, value: float, types: str, lenght:float, width:float,
                height: float, tolerance: float, power_rating: float, description: str):
        super().__init__(name, value, types, height, width, lenght, description)
        self.tolerance = tolerance
        self.power_rating = power_rating

    def breakdown(self, operationPower: float) -> bool:
            return operationPower > self.power_rating