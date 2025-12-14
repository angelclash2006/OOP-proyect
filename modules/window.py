import sys
from PyQt6.QtWidgets import QApplication, QSplitter, QMainWindow, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from pathAssets import ICONS
from component import Component
from workArea import WorkArea
from proyect_manager import ProjectManager
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QFileDialog


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
        rightLayout = QVBoxLayout()
        rightPanel.setLayout(rightLayout)

        saveButton = QPushButton("Save Project")
        loadButton = QPushButton("Load Project")

        rightLayout.addWidget(saveButton)
        rightLayout.addWidget(loadButton)
        rightLayout.addStretch()

        saveButton.clicked.connect(self.save_project)
        loadButton.clicked.connect(self.load_project)


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

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "",
            "Domotic Project (*.json)"
        )

        if path:
            manager = ProjectManager(path)
            manager.save(self.canvasPlaceHolder)
            self.statusBar().showMessage("Project saved successfully")


    def load_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Project",
            "",
            "Domotic Project (*.json)"
        )

        if path:
            manager = ProjectManager(path)
            manager.load(self.canvasPlaceHolder)
            self.statusBar().showMessage("Project loaded successfully")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
