from PyQt6.QtWidgets import QToolButton
from PyQt6.QtCore import Qt, QSize, QMimeData
from PyQt6.QtGui import QIcon, QDrag

class Component(QToolButton):
    def __init__(self, iconPath, componentType, text):
        super().__init__()
        self.componentType = componentType  # Identificador del componente
        self.setText(text)
        self.setIcon(QIcon(iconPath))  # Se usa QIcon directo
        self.setIconSize(QSize(48, 48))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setAcceptDrops(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.MouseButton.LeftButton):
            if (event.position().toPoint() - self.drag_start_position).manhattanLength() < 10:
                return

            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.componentType)  # CamelCase
            drag.setMimeData(mime)

            drag.setPixmap(self.icon().pixmap(self.iconSize()))
            drag.setHotSpot(event.position().toPoint())
            drag.exec(Qt.DropAction.CopyAction)
        else:
            super().mouseMoveEvent(event)