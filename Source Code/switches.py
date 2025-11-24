""" In this module we define the subclass switches,which inherit from the superclass components
and have their own atributtes and methods.
Also we define the diferents subtypes (NO, NC) of switches as subclasses of the switch class."""

from components import Component

class Switch(Component):
    def __init__(self, name: str, value: float, types: str, description: str,
                lenght: float, width: float, height: float,
                normallyClosed: bool, max_current: float):
        super().__init__(name, value, types, lenght, width, height, description)
        self.normallyClosed = normallyClosed  # 'NO' for Normally Open, 'NC' for Normally Closed
        self.max_current = max_current

    def breakdown(self, operationCurrent: float) -> bool:
            return operationCurrent > self.max_current
    
    def toggle(self, button_pressed: bool):
        if self.types == "PressButton":
            while button_pressed:
                self.normallyClosed = not self.normallyClosed

        if self.types == "Toggle":
            if button_pressed:
                self.normallyClosed = not self.normallyClosed            