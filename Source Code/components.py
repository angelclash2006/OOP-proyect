"""In this module we define the superclass components, 
which have the common atributtes and methods of all the components in the project."""

class Component:
    def __init__(self, name: str, value: float, types: str, description: str,
                lenght: float, width: float, height: float):
        self.name = name
        self.value = value
        self.types = types
        self.lenght = lenght
        self.width = width
        self.height = height
        description = description

    def breakdown(self, operationVoltage: float) -> bool:
            return operationVoltage > self.coilVoltage