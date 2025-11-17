"""Into this module are defined the resistors of al type and their caracteristics."""

from components import Component

# In this class,we defin the bassic characteristics of a resistor.
class Resistor(Component):
    def __init__(self, name: str, description: str, type: str, pieceNumber: str,resistance:float, maxPowerRating:float):
        super().__init__(name, description, type, pieceNumber)
        self.resistance = resistance  #in ohms
        self.maxPowerRating = maxPowerRating  #in watts
# Method thad define the characteristics own of each type of resistor
    def resistorInfo(self):
        resistorInfo = self.get_info()
        resistorInfo.update({
            "Resistance": self.resistance,
            "Max Power Rating": self.maxPowerRating
        })
        return resistorInfo
    
# Method that checks if the user input values are valid
    def checkUserResistorValues(self, resistance:float, maxPowerRating:float):
        if resistance <= 0:
            raise ValueError("Resistance must be a positive value.")
        if maxPowerRating <= 0:
            raise ValueError("Max Power Rating must be a positive value.")
        return True

# Method that simulates the breakdown of the resistor under excessive voltage or current
    def resistorBreakdown(self, voltage:float, current:float):
        powerDissipated = voltage * current
        if powerDissipated > (self.resistance * current**2):  # P = I^2 * R
            breakdown=True  # Resistor breaks down
            self.resistance=10e100  # Set resistance to a very high value to simulate open circuit
        else:
            breakdown=False
        return breakdown
