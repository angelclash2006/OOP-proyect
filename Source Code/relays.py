"""In this module we define the relays components class, inheriting from the superclass Component.
This class has the specific attributes and methods of the relays components in the project."""

from components import Component

class Relay(Component):
    def __init__(self, name:str, value:float, types:str, descirption:str,
                lenght:float, width:float, height:float, coilVoltage:float, max_switching_current:float):
        super().__init__(name, value, types, descirption, lenght, width, height)
        self.coilVoltage = coilVoltage
        self.max_switching_current = max_switching_current

    
