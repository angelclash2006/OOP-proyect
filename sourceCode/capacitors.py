"""Into this module are defined the capacitors of all typeOfCap and their caracteristics."""

from components import Component    

class Capacitor(Component):
    def __init__(self,name:str, description:str, typeOfCap:str, pieceNumber:str, capacitance:float, voltageRating:float):
        super().__init__(name, description, pieceNumber)
        self.capacitance = capacitance  #in farads
        self.voltageRating = voltageRating  #in volts
        self.energyStored = 0.5 * self.capacitance * (self.voltageRating ** 2)  #in joules
        self.typeOfCap = typeOfCap    

    def capacitorInfo(self):
        capacitorInfo = self.get_info()
        capacitorInfo.update({
            "Capacitance": self.capacitance,
            "Voltage Rating": self.voltageRating,
            "Energy Stored": self.energyStored,
            "Type of Capacitor": self.typeOfCap
        })
        return capacitorInfo
    
    def checkUserCapacitorValues(self, capacitance:float, voltageRating:float):
        if capacitance <= 0:
            raise ValueError("Capacitance must be a positive value.")
        if voltageRating <= 0:
            raise ValueError("Voltage Rating must be a positive value.")
        return True
    
    def capacitorBreakdown(self, appliedVoltage:float):
        if appliedVoltage > self.voltageRating:
            breakdown = True  # Capacitor breaks down
            self.capacitance = 0  # Set capacitance to zero to simulate failure
        else:
            breakdown = False
        return breakdown