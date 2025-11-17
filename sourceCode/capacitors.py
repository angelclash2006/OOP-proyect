"""Into this module are defined the capacitors of all typeOfCap and their caracteristics."""

from components import Component   

# In this class,we define the bassic characteristics of a capacitor.
class Capacitor(Component):
    def __init__(self,name:str, description:str, typeOfCap:str, pieceNumber:str, capacitance:float, voltageRating:float):
        super().__init__(name, description, pieceNumber)
        self.capacitance = capacitance  #in farads
        self.voltageRating = voltageRating  #in volts
        self.energyStored = 0.5 * self.capacitance * (self.voltageRating ** 2)  #in joules
        self.typeOfCap = typeOfCap    

# Method that define the characteristics own of each type of capacitor
    def capacitorInfo(self):
        capacitorInfo = self.get_info()
        capacitorInfo.update({
            "Capacitance": self.capacitance,
            "Voltage Rating": self.voltageRating,
            "Energy Stored": self.energyStored,
            "Type of Capacitor": self.typeOfCap
        })
        return capacitorInfo
    
# Method that checks if the user input values are valid
    def checkUserCapacitorValues(self, capacitance:float, voltageRating:float):
        if capacitance <= 0:
            raise ValueError("Capacitance must be a positive value.")
        if voltageRating <= 0:
            raise ValueError("Voltage Rating must be a positive value.")
        return True
    
# Method that simulates the breakdown of the capacitor under excessive voltage
    def capacitorBreakdown(self, appliedVoltage:float):
        if appliedVoltage > self.voltageRating:
            breakdown = True  # Capacitor breaks down
            self.capacitance = 0  # Set capacitance to zero to simulate failure
        else:
            breakdown = False
        return breakdown