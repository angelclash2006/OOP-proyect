from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QPointF

class Canvas(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        #tracing
        self.strokes=[]
        self.currentStroke=[]
        
    def paintEvent(self,event):
        painter = QPainter(self)

        painter.drawText(10, 20, "Canvas")
