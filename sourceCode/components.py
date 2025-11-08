"""Super class for designing the components of the model whith the general characteristics."""

class Component:
    def __init__(self, name:str, description: str, pieceNumber:str , parameters: dict, dimensions:dict):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.pieceNumber = pieceNumber
        self.dimensions = dimensions

        def get_info(self):
            info = {
                "Name": self.name,
                "Description": self.description,
                "Piece Number": self.pieceNumber,
                "Parameters": self.parameters,
                "Dimensions": self.dimensions
            }
            return info
