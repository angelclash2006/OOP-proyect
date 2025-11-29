from PyQt6.QtWidgets import QFrame, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from pathAssets import ICONS

class MovableLabel(QLabel):
    def __init__(self, iconPath, name, parent=None):
        super().__init__(parent)
        pixmap = QPixmap(iconPath).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(pixmap)
        self.setToolTip(name)
        self.setStyleSheet("background: transparent;")
        self.setMouseTracking(True)
        self.drag_start_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is None:
                return
            delta = event.position().toPoint() - self.drag_start_position
            new_pos = self.pos() + delta
            self.move(new_pos)

class WorkArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.setMinimumSize(600, 400)

        self.counters = {
            "PushButton": 0,
            "Switch": 0,
            "SourceDC": 0,
            "Motor": 0,
            "Resistor": 0,
            "LED": 0,
            "Diode": 0,
            "GND": 0
        }

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        componentType = event.mimeData().text()
        pos = event.position()

        self.counters[componentType] += 1
        name = f"{componentType}{self.counters[componentType]}"

        iconPath = ICONS.get(componentType)
        if not iconPath:
            print(f"No se encontró el icono para {componentType}")
            return

        label = MovableLabel(iconPath, name, self)
        label.move(int(pos.x()), int(pos.y()))
        label.show()

        event.acceptProposedAction()