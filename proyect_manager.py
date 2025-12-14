import json
from PyQt6.QtCore import QPoint
from workArea import MovableLabel
from pathAssets import ICONS


class ProjectManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, work_area):
        components = []

        for label in work_area.findChildren(MovableLabel):
            components.append({
                "name": label.toolTip(),
                "x": label.x(),
                "y": label.y()
            })

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(components, file, indent=4)

    def load(self, work_area):
        with open(self.file_path, "r", encoding="utf-8") as file:
            components = json.load(file)

        for label in work_area.findChildren(MovableLabel):
            label.deleteLater()

        for data in components:
            name = data["name"]
            component_type = ''.join(filter(str.isalpha, name))
            icon_path = ICONS.get(component_type)

            if not icon_path:
                continue

            label = MovableLabel(icon_path, name, work_area)
            label.move(QPoint(data["x"], data["y"]))
            label.show()

