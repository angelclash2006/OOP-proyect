"""At this module, the relays class is defined, inheriting from the Component class.
The relays are a electromechanical switch that use a coi to create a magnetic
field and open or close the contacts, these switch type are used to control high power"""

from components import Component

class Relay(Component):
    def __init__(self, name: str, description: str, typeOfRelay: str, pieceNumber: str,
                coilVoltage: float, coilCurrent: float, contactConfiguration: str,
                maxSwitchingVoltage: float, maxSwitchingCurrent: float):
        super().__init__(name, description, typeOfRelay, pieceNumber)
        self.coilVoltage = coilVoltage  # in volts
        self.coilCurrent = coilCurrent  # in amperes
        self.contactConfiguration = contactConfiguration  # e.g., SPST, DPDT
        self.maxSwitchingVoltage = maxSwitchingVoltage  # in volts
        self.maxSwitchingCurrent = maxSwitchingCurrent  # in amperes

    def relayInfo(self):
        relay_info = self.get_info()
        relay_info.update({
            "Coil Voltage": self.coilVoltage,
            "Coil Current": self.coilCurrent,
            "Contact Configuration": self.contactConfiguration,
            "Max Switching Voltage": self.maxSwitchingVoltage,
            "Max Switching Current": self.maxSwitchingCurrent
        })
        return relay_info