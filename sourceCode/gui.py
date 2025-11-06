from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QToolBar, QLabel, QPushButton, QMenuBar, QMenu,
                            QDockWidget, QListWidget, QScrollArea, QFrame,
                            QSpinBox, QDoubleSpinBox, QLineEdit, QHBoxLayout,
                            QCheckBox, QFileDialog, QMessageBox, QAction)
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer
from PyQt5.QtGui import QPainter, QPen, QIcon
import sys
import math
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPolygon, QColor
from workSpace import WorkSpace

class DomoticComponent(QLabel):
    def __init__(self, component_type, parent=None):
        super().__init__(parent)
        self.component_type = component_type
        self.setText(component_type)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px solid black;
                background: white;
                border-radius: 5px;
            }
            QLabel:hover {
                border: 2px solid blue;
                background: #f0f0ff;
            }
        """)
        self.setFixedSize(100, 50)
        self.position = QPoint()
        self.connection_points = []
        self.is_being_connected = False
        self.component_id = ""
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ControlModifier:
                # Start connection mode
                self.is_being_connected = True
                self.parent().start_connection(self)
            else:
                # Normal drag mode
                self.start_pos = event.pos()
                self.parent().select_component(self)
            
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and not self.is_being_connected:
            difference = event.pos() - self.start_pos
            new_pos = self.parent().mapFromGlobal(self.mapToGlobal(difference))
            self.move(new_pos)
            # Update connection lines if any
            self.parent().update()
            # update model position in workspace
            try:
                self.parent().workspace.set_component_position(self.component_id, (self.x(), self.y()))
            except Exception:
                pass
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_being_connected:
            self.is_being_connected = False
            self.parent().finish_connection(self)
        else:
            # Snap to grid on release when not connecting
            try:
                self.parent().snap_widget(self)
            except Exception:
                pass
            
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw connection points
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.white)
        
        # Left connection point
        painter.drawEllipse(0, self.height()//2 - 5, 10, 10)
        # Right connection point
        painter.drawEllipse(self.width() - 10, self.height()//2 - 5, 10, 10)
        
        if self.is_being_connected:
            painter.setPen(QPen(Qt.blue, 2, Qt.DashLine))
            painter.drawRect(0, 0, self.width()-1, self.height()-1)
            
    def get_left_connection_point(self) -> QPoint:
        return QPoint(self.x(), self.y() + self.height()//2)
        
    def get_right_connection_point(self) -> QPoint:
        return QPoint(self.x() + self.width(), self.y() + self.height()//2)
            
class WorkspaceWidget(QWidget):
    def __init__(self, workspace: WorkSpace, parent=None):
        super().__init__(parent)
        self.workspace = workspace
        self.setStyleSheet("background-color: #f0f0f0;")
        self.components = []
        self.connections = []  # List of (source_component, target_component) tuples
        self.selected_component = None
        self.connecting_component = None
        self.temp_connection_pos = None
        # Grid settings
        self.show_grid = True
        self.grid_size = 20
        
    def addComponent(self, component_type):
        # determine a default position for the new component
        offset = len(self.components) * 20
        x = 20 + offset
        y = 20 + offset

        component = DomoticComponent(component_type, self)
        component.move(x, y)
        component.show()

        # register in workspace and get the assigned id
        ws_comp = self.workspace.include_component({
            'type': component_type,
            'position': (x, y)
        })
        component.component_id = ws_comp.id
        self.components.append(component)
        
    def select_component(self, component):
        if self.selected_component:
            self.selected_component.setStyleSheet("""
                QLabel {
                    border: 2px solid black;
                    background: white;
                    border-radius: 5px;
                }
                QLabel:hover {
                    border: 2px solid blue;
                    background: #f0f0ff;
                }
            """)
        
        self.selected_component = component
        if component:
            component.setStyleSheet("""
                QLabel {
                    border: 2px solid blue;
                    background: #e0e0ff;
                    border-radius: 5px;
                }
            """)
            # Update properties panel
            if isinstance(self.parent(), QMainWindow):
                # delegate to main window so it can access workspace
                try:
                    self.parent().updateProperties(component)
                except Exception:
                    pass
    
    def start_connection(self, source_component):
        self.connecting_component = source_component
        self.temp_connection_pos = source_component.get_right_connection_point()
        self.update()
        
    def finish_connection(self, target_component):
        if (self.connecting_component and target_component and 
            self.connecting_component != target_component):
            # Add connection to the workspace
            self.workspace.connect_components(
                self.connecting_component.component_id,
                target_component.component_id
            )
            # Add visual connection
            self.connections.append((self.connecting_component, target_component))
        
        self.connecting_component = None
        self.temp_connection_pos = None
        self.update()
        
    def mouseMoveEvent(self, event):
        if self.connecting_component:
            self.temp_connection_pos = event.pos()
            self.update()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # draw grid
        if self.show_grid:
            pen = QPen(QColor(220, 220, 220), 1)
            painter.setPen(pen)
            w = self.width()
            h = self.height()
            for x in range(0, w, self.grid_size):
                painter.drawLine(x, 0, x, h)
            for y in range(0, h, self.grid_size):
                painter.drawLine(0, y, w, y)
        
        # Draw permanent connections
        for source, target in self.connections:
            painter.setPen(QPen(Qt.black, 2))
            start = source.get_right_connection_point()
            end = target.get_left_connection_point()
            painter.drawLine(start, end)
            
            # Draw arrow at target
            painter.setPen(QPen(Qt.black, 1))
            painter.setBrush(Qt.black)
            arrow_size = 8
            angle = 30  # degrees
            dx = end.x() - start.x()
            dy = end.y() - start.y()
            angle_rad = math.atan2(dy, dx)
            arrow_p1 = QPoint(
                end.x() - arrow_size * math.cos(angle_rad - math.radians(angle)),
                end.y() - arrow_size * math.sin(angle_rad - math.radians(angle))
            )
            arrow_p2 = QPoint(
                end.x() - arrow_size * math.cos(angle_rad + math.radians(angle)),
                end.y() - arrow_size * math.sin(angle_rad + math.radians(angle))
            )
            arrow = QPolygon([end, arrow_p1, arrow_p2])
            painter.drawPolygon(arrow)
        
        # Draw temporary connection line while dragging
        if self.connecting_component and self.temp_connection_pos:
            painter.setPen(QPen(Qt.blue, 2, Qt.DashLine))
            start = self.connecting_component.get_right_connection_point()
            painter.drawLine(start, self.temp_connection_pos)

    def snap_widget(self, widget: DomoticComponent):
        """Snap the widget to the nearest grid point and update the workspace model."""
        gx = round(widget.x() / self.grid_size) * self.grid_size
        gy = round(widget.y() / self.grid_size) * self.grid_size
        widget.move(gx, gy)
        # update model
        try:
            if hasattr(self, 'workspace') and getattr(widget, 'component_id', None):
                self.workspace.set_component_position(widget.component_id, (gx, gy))
        except Exception:
            pass
        self.update()

class ComponentList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addComponents()
        
    def addComponents(self):
        components = [
            ("Lamp", "lamp.png"),
            ("Switch", "switch.png"),
            ("Socket", "socket.png"),
            ("Relay", "relay.png"),
            ("Fan", "fan.png"),
            ("Light Sensor", "light_sensor.png"),
            ("Thermostat", "thermostat.png"),
            ("Display", "display.png")
        ]
        
        for name, icon in components:
            item = QLabel(name)
            item.setAlignment(Qt.AlignCenter)
            self.addItem(name)

class PropertiesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Title
        title = QLabel("Properties")
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        self.layout.addWidget(title)
        
        # Placeholder content
        self.message = QLabel("Select a component to see its properties")
        self.message.setWordWrap(True)
        self.layout.addWidget(self.message)

    def update_properties(self, gui_component=None, model_component=None):
        # Clear existing widgets (except the title)
        while self.layout.count() > 1:
            item = self.layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        if not gui_component:
            self.message.show()
            return

        self.message.hide()

        # Show basic GUI component info
        self.layout.addWidget(QLabel(f"ID: {getattr(gui_component, 'component_id', '')}"))
        self.layout.addWidget(QLabel(f"Type: {getattr(gui_component, 'component_type', '')}"))
        self.layout.addWidget(QLabel(f"Position: ({gui_component.x()}, {gui_component.y()})"))

        # Show model properties if available
        if model_component:
            props = model_component.properties
            if props:
                self.layout.addWidget(QLabel("Properties:"))
                # create editable widgets for each property
                self._prop_widgets = {}
                for k, v in props.items():
                    row = QHBoxLayout()
                    label = QLabel(k)
                    row.addWidget(label)
                    if isinstance(v, bool):
                        widget = QCheckBox()
                        widget.setChecked(bool(v))
                    elif isinstance(v, int):
                        widget = QSpinBox()
                        widget.setValue(int(v))
                    elif isinstance(v, float):
                        widget = QDoubleSpinBox()
                        widget.setValue(float(v))
                    else:
                        widget = QLineEdit(str(v))
                    row.addWidget(widget)
                    container = QWidget()
                    container.setLayout(row)
                    self.layout.addWidget(container)
                    self._prop_widgets[k] = widget

                # Save button
                save_btn = QPushButton("Save Properties")
                def on_save():
                    new_props = {}
                    for key, w in self._prop_widgets.items():
                        if isinstance(w, QCheckBox):
                            new_props[key] = w.isChecked()
                        elif isinstance(w, QSpinBox) or isinstance(w, QDoubleSpinBox):
                            new_props[key] = w.value()
                        else:
                            new_props[key] = w.text()
                    # persist to workspace model
                    try:
                        if hasattr(self, 'workspace') and model_component:
                            self.workspace.update_component(model_component.id, new_props)
                            QMessageBox.information(self, 'Properties', 'Properties saved')
                    except Exception as e:
                        QMessageBox.warning(self, 'Properties', f'Failed to save: {e}')

                save_btn.clicked.connect(on_save)
                self.layout.addWidget(save_btn)

class HomeAutomationSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Automation Circuit Simulator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create WorkSpace instance
        self.workspace = WorkSpace(
            [],  # components
            1,   # projectID
            "New Project",  # projectName
            "Home automation circuit simulator",  # projectDescription
            [800, 600],  # spaceDimensions
            "px",  # measureUnits
            100,  # zoom
            [],   # nets
            [],   # controllers
            False,  # simulationState
            0.0,    # simulationTime
            False,  # simulationMode
            [],     # logs
            "default",  # user
            ["light"],  # theme
            ""      # lastModified
        )
        
        self.setupUI()
        # current open file
        self.current_file = None
        # simulation timer
        self.sim_timer = QTimer(self)
        self.sim_timer.setInterval(500)  # ms
        self.sim_timer.timeout.connect(self.simulation_step)
        # autosave every 10s when a file is open
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(10000)
        """Save the workspace automatically to the current file if set."""
        if self.current_file:
            try:
                self.workspace.save_to_file(self.current_file)
                # optionally show a subtle status update
                self.statusBar().showMessage(f"Autosaved to {self.current_file}", 2000)
            except Exception:
                pass
        
    def setupUI(self):
        # Create menu bar
        self.createMenuBar()
        
        # Create toolbar
        self.createToolBar()
        
        # Create workspace
        self.workspace_widget = WorkspaceWidget(self.workspace)
        self.setCentralWidget(self.workspace_widget)
        
        # Create properties dock widget (left side)
        properties_dock = QDockWidget("Properties", self)
        self.properties_panel = PropertiesPanel()
        # give properties panel access to the workspace model
        self.properties_panel.workspace = self.workspace
        properties_dock.setWidget(self.properties_panel)
        properties_dock.setFeatures(QDockWidget.DockWidgetFloatable | 
                                    QDockWidget.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, properties_dock)
        
        # Create components dock widget (right side)
        components_dock = QDockWidget("Components", self)
        self.components_list = ComponentList()
        components_dock.setWidget(self.components_list)
        components_dock.setFeatures(QDockWidget.DockWidgetFloatable | 
                                QDockWidget.DockWidgetMovable)
        self.addDockWidget(Qt.RightDockWidgetArea, components_dock)

        # connect double-click on a component name to add it to workspace
        self.components_list.itemDoubleClicked.connect(
            lambda item: self.workspace_widget.addComponent(item.text())
        )

    def updateProperties(self, component_widget):
        """Called by WorkspaceWidget when a component is selected."""
        # Find the workspace component model
        comp_id = getattr(component_widget, 'component_id', None)
        model_comp = None
        if comp_id:
            model_comp = self.workspace.get_component(comp_id)
        # Delegate to properties panel
        try:
            self.properties_panel.update_properties(component_widget, model_comp)
        except Exception:
            pass

    # ---------------------- File actions ----------------------
    def new_project(self):
        # Reset workspace and GUI
        self.workspace = WorkSpace([], 1, "New Project", "", [800,600], "px", 100, [], [], False, 0.0, False, [], "default", ["light"], "")
        # clear GUI
        self.workspace_widget.components.clear()
        for child in self.workspace_widget.findChildren(DomoticComponent):
            child.deleteLater()
        self.workspace_widget.connections.clear()
        self.workspace_widget.update()
        self.current_file = None

    def open_project(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "JSON Files (*.json);;All Files (*)")
        if not fname:
            return
        ws = WorkSpace.load_from_file(fname)
        if not ws:
            QMessageBox.warning(self, "Open Project", "Failed to open project")
            return
        self.workspace = ws
        self.current_file = fname
        self.load_workspace_into_gui()

    def save_project(self):
        if not self.current_file:
            return self.save_project_as()
        ok = self.workspace.save_to_file(self.current_file)
        if not ok:
            QMessageBox.warning(self, "Save Project", "Failed to save project")
        else:
            QMessageBox.information(self, "Save Project", f"Saved to {self.current_file}")

    def save_project_as(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Save Project As", "", "JSON Files (*.json);;All Files (*)")
        if not fname:
            return
        ok = self.workspace.save_to_file(fname)
        if ok:
            self.current_file = fname
            QMessageBox.information(self, "Save Project", f"Saved to {fname}")
        else:
            QMessageBox.warning(self, "Save Project", "Failed to save project")

    # ---------------------- Simulation controls ----------------------
    def start_simulation(self):
        if not self.sim_timer.isActive():
            self.sim_timer.start()

    def pause_simulation(self):
        if self.sim_timer.isActive():
            self.sim_timer.stop()

    def stop_simulation(self):
        if self.sim_timer.isActive():
            self.sim_timer.stop()
        # optionally reset simulation state
        QMessageBox.information(self, "Simulation", "Simulation stopped")

    def simulation_step(self):
        # Delegate to workspace simulation logic
        try:
            self.workspace.run_simulation_step()
        except Exception:
            pass
        # Refresh GUI visual state to reflect model
        self.update_visuals_from_model()

    def update_visuals_from_model(self):
        """Update each widget's visual appearance based on the model properties."""
        # Map component_id -> model component
        model_map = {c.id: c for c in self.workspace.get_components()}
        for widget in self.workspace_widget.components:
            mc = model_map.get(getattr(widget, 'component_id', None))
            if not mc:
                continue
            # Default appearance
            style = "border: 2px solid black; background: white; border-radius: 5px;"
            # Visual rules
            state = mc.properties.get('state')
            sim_state = mc.properties.get('sim_state')
            effective = sim_state or state
            if mc.type == 'LED':
                if str(effective).lower() == 'on' or effective == True:
                    style = "border: 2px solid orange; background: yellow; border-radius: 5px;"
                else:
                    style = "border: 2px solid black; background: white; border-radius: 5px;"
            elif mc.type == 'Relay':
                if str(effective).lower() == 'on' or effective == True:
                    style = "border: 2px solid green; background: #eaffea; border-radius: 5px;"
            elif mc.type == 'PowerSource':
                style = "border: 2px solid red; background: #ffecec; border-radius: 5px;"
            elif mc.type == 'Switch':
                s = mc.properties.get('state', False)
                if s == True or str(s).lower() == 'on':
                    style = "border: 2px solid blue; background: #e0f0ff; border-radius: 5px;"
            widget.setStyleSheet(style)
        # repaint
        self.workspace_widget.update()

    def load_workspace_into_gui(self):
        # clear existing GUI components
        for child in self.workspace_widget.findChildren(DomoticComponent):
            child.deleteLater()
        self.workspace_widget.components.clear()
        self.workspace_widget.connections.clear()

        # recreate components from model
        for model_comp in self.workspace.get_components():
            w = DomoticComponent(model_comp.type, self.workspace_widget)
            x, y = model_comp.position
            w.move(int(x), int(y))
            w.component_id = model_comp.id
            w.show()
            self.workspace_widget.components.append(w)

        # recreate connections visually
        for model_comp in self.workspace.get_components():
            for cid in model_comp.connections:
                src_widget = next((w for w in self.workspace_widget.components if w.component_id == model_comp.id), None)
                tgt_widget = next((w for w in self.workspace_widget.components if w.component_id == cid), None)
                if src_widget and tgt_widget:
                    self.workspace_widget.connections.append((src_widget, tgt_widget))

        self.workspace_widget.update()
        
    def createMenuBar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        new_act = QAction("New Project", self)
        open_act = QAction("Open Project...", self)
        save_act = QAction("Save", self)
        save_as_act = QAction("Save As...", self)
        exit_act = QAction("Exit", self)
        file_menu.addAction(new_act)
        file_menu.addAction(open_act)
        file_menu.addAction(save_act)
        file_menu.addAction(save_as_act)
        file_menu.addSeparator()
        file_menu.addAction(QAction("Export...", self))
        file_menu.addAction(QAction("Import...", self))
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

        # connect file actions
        new_act.triggered.connect(self.new_project)
        open_act.triggered.connect(self.open_project)
        save_act.triggered.connect(self.save_project)
        save_as_act.triggered.connect(self.save_project_as)
        exit_act.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")
        edit_menu.addAction("Delete")
        edit_menu.addSeparator()
        edit_menu.addAction("Select All")
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Zoom In")
        view_menu.addAction("Zoom Out")
        view_menu.addAction("Fit to Screen")
        view_menu.addSeparator()
        view_menu.addAction("Show Grid")
        view_menu.addAction("Show Connection Points")
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Connect Components")
        tools_menu.addAction("Align Components")
        tools_menu.addAction("Group Components")
        tools_menu.addSeparator()
        tools_menu.addAction("Validate Circuit")
        
        # Preferences menu
        preferences_menu = menubar.addMenu("Preferences")
        preferences_menu.addAction("Settings...")
        preferences_menu.addAction("Customize Toolbar...")
        preferences_menu.addAction("Keyboard Shortcuts...")
        theme_menu = preferences_menu.addMenu("Theme")
        theme_menu.addAction("Light")
        theme_menu.addAction("Dark")
        theme_menu.addAction("System")
        
        # Simulation menu
        simulation_menu = menubar.addMenu("Simulation")
        self.sim_start_act = QAction("Start", self)
        self.sim_pause_act = QAction("Pause", self)
        self.sim_stop_act = QAction("Stop", self)
        simulation_menu.addAction(self.sim_start_act)
        simulation_menu.addAction(self.sim_pause_act)
        simulation_menu.addAction(self.sim_stop_act)
        simulation_menu.addSeparator()
        simulation_menu.addAction("Step Forward")
        simulation_menu.addAction("Step Backward")
        simulation_menu.addSeparator()
        simulation_menu.addAction("Configuration...")
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation")
        help_menu.addAction("Tutorials")
        help_menu.addAction("Component Library")
        help_menu.addSeparator()
        help_menu.addAction("Check for Updates...")
        help_menu.addSeparator()
        help_menu.addAction("About")
        
    def createToolBar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        # Add toolbar actions (you can add icons later)
        actions = [
            ("Run", "run.png"),
            ("Settings", "settings.png"),
            ("Connect", "connect.png"),
            ("Share", "share.png"),
            ("Search", "search.png"),
            ("Undo", "undo.png"),
            ("Light", "light.png"),
            ("Dark", "dark.png")
        ]
        
        for name, icon in actions:
            action = toolbar.addAction(name)

        # connect simulation actions
        try:
            self.sim_start_act.triggered.connect(self.start_simulation)
            self.sim_pause_act.triggered.connect(self.pause_simulation)
            self.sim_stop_act.triggered.connect(self.stop_simulation)
        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomeAutomationSimulator()
    window.show()
    sys.exit(app.exec_())