"""
Module for defining specific component types and their behaviors.
"""
from dataclasses import dataclass
from typing import Dict, Any, List
from abc import ABC, abstractmethod

class DomoticComponent(ABC):
    """Abstract base class for all domotic components"""
    def __init__(self, id: str, position: tuple[float, float]):
        self.id = id
        self.position = position
        self.connections: List[str] = []
        self._state = False

    @property
    def state(self) -> bool:
        return self._state

    @state.setter
    def state(self, value: bool):
        self._state = value
        self.on_state_change()

    @abstractmethod
    def on_state_change(self):
        """Called when the component's state changes"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'position': self.position,
            'state': self.state,
            'connections': self.connections
        }

class PowerSource(DomoticComponent):
    """Represents a power source component"""
    def __init__(self, id: str, position: tuple[float, float], voltage: float = 12.0):
        super().__init__(id, position)
        self.voltage = voltage
        self._state = True  # Power sources are always on by default

    def on_state_change(self):
        # Notify connected components about power state
        pass

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['voltage'] = self.voltage
        return data

class LED(DomoticComponent):
    """Represents an LED component"""
    def __init__(self, id: str, position: tuple[float, float], color: str = 'white'):
        super().__init__(id, position)
        self.color = color
        self.brightness = 0

    def on_state_change(self):
        if self.state:
            self.brightness = 100
        else:
            self.brightness = 0

    def set_brightness(self, value: int):
        self.brightness = max(0, min(100, value))
        self.state = self.brightness > 0

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'color': self.color,
            'brightness': self.brightness
        })
        return data

class Switch(DomoticComponent):
    """Represents a switch component"""
    def __init__(self, id: str, position: tuple[float, float], switch_type: str = 'toggle'):
        super().__init__(id, position)
        self.switch_type = switch_type  # toggle or momentary

    def toggle(self):
        self.state = not self.state

    def press(self):
        if self.switch_type == 'momentary':
            self.state = True
        else:
            self.toggle()

    def release(self):
        if self.switch_type == 'momentary':
            self.state = False

    def on_state_change(self):
        # Notify connected components
        pass

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['switch_type'] = self.switch_type
        return data

class Relay(DomoticComponent):
    """Represents a relay component"""
    def __init__(self, id: str, position: tuple[float, float], max_current: float = 10.0):
        super().__init__(id, position)
        self.max_current = max_current
        self.current_load = 0.0

    def on_state_change(self):
        # Notify connected components about relay state
        pass

    def set_load(self, current: float):
        if current <= self.max_current:
            self.current_load = current
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'max_current': self.max_current,
            'current_load': self.current_load
        })
        return data

class MotionSensor(DomoticComponent):
    """Represents a motion sensor component"""
    def __init__(self, id: str, position: tuple[float, float], sensitivity: int = 5):
        super().__init__(id, position)
        self.sensitivity = sensitivity
        self.detection_range = 5.0  # meters
        self.last_detection = None

    def detect_motion(self, presence: bool):
        if presence and self.sensitivity > 0:
            self.state = True
        else:
            self.state = False

    def on_state_change(self):
        # Trigger connected components when motion is detected
        pass

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'sensitivity': self.sensitivity,
            'detection_range': self.detection_range
        })
        return data

# Function to create components by type
def create_component(component_type: str, id: str, position: tuple[float, float], **kwargs) -> DomoticComponent:
    """Factory function to create components by type"""
    component_classes = {
        'PowerSource': PowerSource,
        'LED': LED,
        'Switch': Switch,
        'Relay': Relay,
        'MotionSensor': MotionSensor
    }
    
    if component_type not in component_classes:
        raise ValueError(f"Unknown component type: {component_type}")
    
    return component_classes[component_type](id, position, **kwargs)