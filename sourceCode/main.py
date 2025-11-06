"""
Main module to test the components and workspace functionality.
"""
from workSpace import WorkSpace
from components import create_component
import sys
from PyQt5.QtWidgets import QApplication
from gui import HomeAutomationSimulator

def test_components():
    # Create a workspace
    workspace = WorkSpace(
        components=[],
        projectID=1,
        projectName="Test Project",
        projectDescription="Testing components",
        spaceDimensions=[800, 600],
        measureUnits="px",
        zoom=100,
        nets=[],
        controllers=[],
        simulationState=False,
        simulationTime=0.0,
        simulationMode=False,
        logs=[],
        user="test_user",
        theme=["light"],
        lastModified=""
    )

    # Create some components
    power = create_component("PowerSource", "power1", (100, 100), voltage=12.0)
    led1 = create_component("LED", "led1", (200, 100), color="red")
    switch1 = create_component("Switch", "switch1", (150, 150))
    relay1 = create_component("Relay", "relay1", (250, 150))
    motion1 = create_component("MotionSensor", "motion1", (300, 100))

    # Add components to workspace
    for component in [power, led1, switch1, relay1, motion1]:
        workspace.include_component(component.to_dict())

    # Create some connections
    workspace.connect_components("power1", "relay1")
    workspace.connect_components("relay1", "led1")
    workspace.connect_components("switch1", "relay1")
    workspace.connect_components("motion1", "relay1")

    # Test component interactions
    print("\nTesting components:")
    print("1. Initial state:")
    for comp in workspace.get_components():
        print(f"  - {comp.id} ({comp.type}): connected to {comp.connections}")

    # Validate circuit
    print("\n2. Circuit validation:")
    errors = workspace.validate_circuit()
    if errors:
        print("Circuit validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Circuit validation passed!")

    return workspace

def main():
    # Create Qt Application
    app = QApplication(sys.argv)
    
    # Create and test components
    workspace = test_components()
    
    # Create and show the main window
    window = HomeAutomationSimulator()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
