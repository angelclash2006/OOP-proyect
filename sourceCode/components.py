"""Super class for designing the components of the model whith the general characteristics."""
# Here is defined the Component class that will be the super class for all the components of the model.
class Component:
    def __init__(self, name:str, description: str, pieceNumber:str ,
                parameters: dict, dimensions:dict):
        self.name = name
        self.description = description
        self.parameters = {"Power": None, "Voltage": None, "Current": None}
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
