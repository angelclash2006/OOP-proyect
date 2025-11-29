from capacitors import Capacitor
from resistors import Resistor
from motors import Motor
from relays import Relay
from switches import Switch

C1 = Capacitor("C1", 1, "Electrolytic", 0.5, 0.3, 0.2, 16, "General purpose capacitor")
testVoltage=20

print(f"Testing breakdown for capacitor {C1.name} with voltage rating {C1.voltageRating}V at {testVoltage}V")

if C1.breakdown(testVoltage):
    print(f"The capacitor {C1.name} has broken down at {testVoltage}V")

    #test all


