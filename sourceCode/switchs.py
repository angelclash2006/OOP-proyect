"""Into this module are defined the stwitches of all typeOfSw and their caracteristics.
Importantly, in this module we need differenciate between mechanical and electronic switches
Also, we need to define the different typeOfSws of switches, like toggle, push button and their sub typeOfSws, 
normally open or normally close."""

from components import Component

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

    def switchInfo(self):
        switch_info = self.get_info()
        switch_info.update({
            "Switch typeOfSw": self.switchtypeOfSw,
            "Max Voltage": self.maxVoltage,
            "Max Current": self.maxCurrent
        })
        return switch_info
    