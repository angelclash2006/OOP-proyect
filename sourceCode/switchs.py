"""Into this module are defined the stwitches of all typeOfSw and their caracteristics.
Importantly, in this module we need differenciate between mechanical and electronic switches
Also, we need to define the different typeOfSws of switches, like toggle, push button and their sub typeOfSws, 
normally open or normally close."""

from components import Component

# In this class,we defin the bassic characteristics of a switch.
class Switch(Component):
    def __init__(self, name: str, description: str, typeOfSw: str, pieceNumber: str, switchtypeOfSw: str,
                maxVoltage: float, maxCurrent: float, defaultState: str, toggleType: str):
        super().__init__(name, description, typeOfSw, pieceNumber)
        self.switchtypeOfSw = switchtypeOfSw  # e.g., toggle, push button
        self.maxVoltage = maxVoltage  # in volts
        self.maxCurrent = maxCurrent  # in amperes
        self.typeOfSw = typeOfSw  # e.g., mechanical, electronic
        self.defaultState = defaultState
        self.toggleType = toggleType

# Method thad define the characteristics own of each type of switch
    def switchInfo(self):
        switch_info = self.get_info()
        switch_info.update({
            "Switch typeOfSw": self.switchtypeOfSw,
            "Max Voltage": self.maxVoltage,
            "Max Current": self.maxCurrent
        })
        return switch_info
    
# Method that checks if the user input values are valid
    def checkUserSwitchValues(self, maxVoltage: float, maxCurrent: float):
        if maxVoltage <= 0:
            raise ValueError("Max Voltage must be a positive value.")
        if maxCurrent <= 0:
            raise ValueError("Max Current must be a positive value.")
        return True     

# Method that simulates the breakdown of the switch under excessive voltage or current
    def switchBreakdown(self, voltage: float, current: float):
        if voltage > self.maxVoltage or current > self.maxCurrent:
            breakdown = True  # Switch breaks down
            self.defaultState = "broken"  # Set state to broken to simulate failure
        else:
            breakdown = False
        return breakdown