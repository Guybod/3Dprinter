"""MainApp"""

from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout

from page.action.TemperatureAction import TemperatureAction
from page.action.plainTextEditAction import PlainTextEditAction

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.center_layout = None
        self.central_widget = None
        self.temperature = None
        self.log = None
        self.init_ui()
        self.init_layout()
        self.bind()

    def init_ui(self):
        self.temperature = TemperatureAction()
        self.log = PlainTextEditAction()

    def init_layout(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.center_layout = QVBoxLayout(self.central_widget)
        self.center_layout.addWidget(self.temperature)
        self.center_layout.addWidget(self.log)

    def bind(self):
        self.log.bind(self.temperature)