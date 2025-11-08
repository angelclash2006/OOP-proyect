"""From the components module, import the Component class.
and using the Component class, create a PowerSource class that inherits from it."""
from components import Component

class PowerSource(Component):
    """Class to model power sources, inheriting from Component."""

    def __init__(self, name: str, description: str, type: str, pieceNumber: str, 
                parameters: dict, dimensions: dict, voltage: float, current: float):
        super().__init__(name, description, type, pieceNumber, parameters, dimensions)
        self.voltage = voltage  #in volts
        self.current = current    #in amperes
        self.power = self.voltage * self.current   #in watts

    def suppyInfo(self):
        power_info = self.get_info()
        power_info.update({
            "Voltage": self.voltage,
            "Current": self.current,
            "Power": self.power,
            })
        return power_info
