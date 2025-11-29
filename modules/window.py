import sys
from PyQt6.QtWidgets import QApplication, QSplitter, QMainWindow, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from pathAssets import ICONS
from component import Component
from workArea import WorkArea

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Domotic circuit simulator")
        self.setGeometry(0, 0, 900, 600)
        self.statusBar().showMessage("Ready test")

        # Paneles
        leftPanel = QFrame()
        leftPanel.setFrameShape(QFrame.Shape.StyledPanel)
        rightPanel = QFrame()
        rightPanel.setFrameShape(QFrame.Shape.StyledPanel)
        self.canvasPlaceHolder = WorkArea()

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(leftPanel)
        splitter.addWidget(self.canvasPlaceHolder)
        splitter.addWidget(rightPanel)
        splitter.setSizes([160, 900, 160])
        self.setCentralWidget(splitter)
        self.statusBar().showMessage("Made by YOTAS")

        # Grid de componentes
        componentsGrid = QGridLayout(leftPanel)
        leftPanel.setLayout(componentsGrid)

        buttons = [
            ("PushButton", "Push Button"),
            ("Switch", "Switch"),
            ("SourceDC", "DC Source"),
            ("Motor", "Motor"),
            ("Resistor", "Resistor"),
            ("LED", "LED"),
            ("Diode", "Diode"),
            ("GND", "GND")
        ]

        row, col = 0, 0
        for compType, text in buttons:
            btn = Component(ICONS[compType], compType, text)
            componentsGrid.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())