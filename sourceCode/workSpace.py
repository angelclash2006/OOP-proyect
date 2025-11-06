"""
Module for managing a workspace environment.
Defines the WorkSpace class with initialization parameters
 and component management.
"""
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class Component:
    """Class to represent a component in the workspace"""
    id: str
    type: str
    position: Tuple[float, float]
    properties: Dict[str, Any]
    connections: List[str]  # List of connected component IDs

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type,
            'position': self.position,
            'properties': self.properties,
            'connections': self.connections
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Component':
        return cls(
            id=data['id'],
            type=data['type'],
            position=tuple(data['position']),
            properties=data['properties'],
            connections=data['connections']
        )

class WorkSpace:
    def __init__(self, components: List[Any], projectID: int, projectName: str,
                 projectDescription: str, spaceDimensions: List[float], measureUnits: str,
                 zoom: int, nets: List[str], controllers: List[str], simulationState: bool,
                 simulationTime: float, simulationMode: bool, logs: List[Any], user: str,
                 theme: List[str], lastModified: str):
        self.components: List[Component] = []
        self.projectID = projectID
        self.projectName = projectName
        self.projectDescription = projectDescription
        self.spaceDimensions = spaceDimensions
        self.measureUnits = measureUnits
        self.zoom = zoom
        self.nets = nets
        self.controllers = controllers
        self.simulationState = simulationState
        self.simulationTime = simulationTime
        self.simulationMode = simulationMode
        self.logs = logs
        self._user = user
        self.theme = theme
        self.lastModified = lastModified or datetime.now().isoformat()
        self._next_component_id = 1

    def generate_component_id(self) -> str:
        """Generate a unique ID for a new component"""
        component_id = f"comp_{self._next_component_id}"
        self._next_component_id += 1
        return component_id

    def include_component(self, component_data: Dict[str, Any]) -> Component:
        """Add a new component to the workspace"""
        # Generate default properties based on component type
        default_properties = self._get_default_properties(component_data['type'])
        
        # Create new component
        component = Component(
            id=self.generate_component_id(),
            type=component_data['type'],
            position=component_data.get('position', (0, 0)),
            properties=default_properties,
            connections=[]
        )
        
        self.components.append(component)
        self.lastModified = datetime.now().isoformat()
        return component

    def _get_default_properties(self, component_type: str) -> Dict[str, Any]:
        """Get default properties for a component type"""
        default_properties = {
            'Lamp': {
                'state': 'off',
                'brightness': 0,
                'max_brightness': 100,
                'power': 60  # watts
            },
            'Switch': {
                'state': 'off',
                'type': 'toggle'
            },
            'Socket': {
                'state': 'off',
                'max_power': 1000  # watts
            },
            'Relay': {
                'state': 'off',
                'max_current': 10  # amperes
            },
            'Fan': {
                'state': 'off',
                'speed': 0,
                'max_speed': 5
            },
            'Light Sensor': {
                'threshold': 500,  # lux
                'current_value': 0
            },
            'Thermostat': {
                'temperature': 20,  # Celsius
                'target_temperature': 22,
                'mode': 'heat'  # heat/cool/off
            },
            'Display': {
                'text': '',
                'backlight': True
            }
        }
        return default_properties.get(component_type, {})

    def update_component(self, component_id: str, properties: Dict[str, Any]) -> bool:
        """Update a component's properties"""
        for component in self.components:
            if component.id == component_id:
                component.properties.update(properties)
                self.lastModified = datetime.now().isoformat()
                return True
        return False

    def set_component_position(self, component_id: str, position: Tuple[float, float]) -> bool:
        """Update a component's position in the workspace model"""
        for component in self.components:
            if component.id == component_id:
                component.position = position
                self.lastModified = datetime.now().isoformat()
                return True
        return False

    def remove_component(self, component_id: str) -> bool:
        """Remove a component from the workspace"""
        for component in self.components:
            if component.id == component_id:
                # Remove connections to this component
                for other_component in self.components:
                    if component_id in other_component.connections:
                        other_component.connections.remove(component_id)
                
                self.components.remove(component)
                self.lastModified = datetime.now().isoformat()
                return True
        return False

    def connect_components(self, source_id: str, target_id: str) -> bool:
        """Create a connection between two components"""
        source = self.get_component(source_id)
        target = self.get_component(target_id)
        
        if source and target:
            if target_id not in source.connections:
                source.connections.append(target_id)
                self.lastModified = datetime.now().isoformat()
                return True
        return False

    def disconnect_components(self, source_id: str, target_id: str) -> bool:
        """Remove a connection between two components"""
        source = self.get_component(source_id)
        
        if source and target_id in source.connections:
            source.connections.remove(target_id)
            self.lastModified = datetime.now().isoformat()
            return True
        return False

    def get_component(self, component_id: str) -> Optional[Component]:
        """Get a component by its ID"""
        for component in self.components:
            if component.id == component_id:
                return component
        return None

    def get_connected_components(self, component_id: str) -> List[Component]:
        """Get all components connected to a specific component"""
        component = self.get_component(component_id)
        if not component:
            return []
        
        return [self.get_component(conn_id) for conn_id in component.connections
                if self.get_component(conn_id)]

    def save_to_file(self, filename: str) -> bool:
        """Save the workspace to a file"""
        try:
            data = {
                'projectID': self.projectID,
                'projectName': self.projectName,
                'projectDescription': self.projectDescription,
                'spaceDimensions': self.spaceDimensions,
                'measureUnits': self.measureUnits,
                'zoom': self.zoom,
                'nets': self.nets,
                'controllers': self.controllers,
                'simulationState': self.simulationState,
                'simulationTime': self.simulationTime,
                'simulationMode': self.simulationMode,
                'components': [comp.to_dict() for comp in self.components],
                'user': self._user,
                'theme': self.theme,
                'lastModified': self.lastModified
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving workspace: {e}")
            return False

    @classmethod
    def load_from_file(cls, filename: str) -> Optional['WorkSpace']:
        """Load a workspace from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            workspace = cls(
                components=[],  # Will be loaded below
                projectID=data['projectID'],
                projectName=data['projectName'],
                projectDescription=data['projectDescription'],
                spaceDimensions=data['spaceDimensions'],
                measureUnits=data['measureUnits'],
                zoom=data['zoom'],
                nets=data['nets'],
                controllers=data['controllers'],
                simulationState=data['simulationState'],
                simulationTime=data['simulationTime'],
                simulationMode=data['simulationMode'],
                logs=[],
                user=data['user'],
                theme=data['theme'],
                lastModified=data['lastModified']
            )
            
            # Load components
            for comp_data in data['components']:
                component = Component.from_dict(comp_data)
                workspace.components.append(component)
            
            return workspace
        except Exception as e:
            print(f"Error loading workspace: {e}")
            return None

    def validate_circuit(self) -> List[str]:
        """Validate the current circuit configuration"""
        errors = []
        
        # Check for components without connections
        for component in self.components:
            if not component.connections:
                errors.append(f"Component {component.id} ({component.type}) has no connections")
        
        # Check for invalid connections
        for component in self.components:
            for conn_id in component.connections:
                if not self.get_component(conn_id):
                    errors.append(f"Component {component.id} has invalid connection to {conn_id}")
        
        return errors

    def run_simulation_step(self) -> None:
        """Run a simple simulation propagation step.

        Rules (simple prototype):
        - PowerSource components are sources of power.
        - A powered Relay or LED will have property 'state' set to 'on'.
        - A Switch passes power if its property 'state' is 'on'.
        - Propagation follows directed connections from source -> target.
        """
        # reset transient states
        for comp in self.components:
            # we keep persisted properties like 'state', but allow override during sim
            if 'sim_state' in comp.properties:
                comp.properties.pop('sim_state', None)

        # BFS from all power sources
        queue: List[Component] = [c for c in self.components if c.type == 'PowerSource']
        visited = set()

        while queue:
            current = queue.pop(0)
            visited.add(current.id)
            # Mark current as powered
            current.properties['sim_state'] = 'on'
            # Propagate to connections
            for cid in current.connections:
                target = self.get_component(cid)
                if not target or target.id in visited:
                    continue
                # If target is a Switch, check its user-set state
                if target.type == 'Switch':
                    # check stored property 'state' (bool or 'on'/'off')
                    s = target.properties.get('state', False)
                    is_on = (s == True) or (str(s).lower() == 'on')
                    if is_on:
                        target.properties['sim_state'] = 'on'
                        queue.append(target)
                else:
                    # For Relay and LED and others, power them and continue
                    target.properties['sim_state'] = 'on'
                    queue.append(target)

        # After propagation, sync sim_state into persistent 'state' for some components
        for comp in self.components:
            sim = comp.properties.get('sim_state')
            if sim == 'on':
                comp.properties['state'] = 'on'
            else:
                # only clear persistent state for components that are not sources
                if comp.type != 'PowerSource':
                    comp.properties['state'] = comp.properties.get('state', 'off')

    def get_components(self) -> List[Component]:
        return self.components

    def get_component_by_position(self, x: float, y: float, tolerance: float = 5.0) -> Optional[Component]:
        """Find a component at the given position with some tolerance"""
        for component in self.components:
            comp_x, comp_y = component.position
            if (abs(comp_x - x) <= tolerance and 
                abs(comp_y - y) <= tolerance):
                return component
        return None