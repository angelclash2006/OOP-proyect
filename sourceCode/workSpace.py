"""
Module for managing a workspace environment.
Defines the WorkSpace class with initialization parameters.
"""
from typing import List
class WorkSpace:
    def __init__ (self,projectID:int, projectName:str,projectDescription:str, 
                spaceDimensions:List[float], measureUnits:str, zoom:int, nets:List[str], 
                controllers:List[str], simulationState:bool, simulationTime:float, 
                simulationMode:bool, logs, user, theme:List[str], lastModified:str):
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
        self.user = user
        self.theme = theme
        self.lastModified = lastModified