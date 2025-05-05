from PySide6.QtWidgets import QLabel, QHBoxLayout, QLineEdit
from PySide6.QtGui import QIntValidator

from page.base.base_frame import BaseFrame


class TemperatureFrame(BaseFrame):
    def __init__(self,name):
        super().__init__()
        self.name = name
        self.setup_ui()

    def init_ui(self):
        self.temperature_label = QLabel(self.name)
        self.current_temperature_label = QLabel("25℃ /")
        self.set_temperature_line_edit = QLineEdit()
        self.set_temperature_line_edit.setFixedSize(225, 30)
        self.set_temperature_line_edit.setMaximumSize(225, 30)
        self.intvalidator = QIntValidator(-235, 500)
        self.set_temperature_line_edit.setValidator(self.intvalidator) 
        self.set_temperature_line_edit.setPlaceholderText("请输入设定温度(1~600)")
        self.signal_label = QLabel("℃")

    def init_layout(self):
        layout = QHBoxLayout(self)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.current_temperature_label)
        layout.addWidget(self.set_temperature_line_edit)
        layout.addWidget(self.signal_label)


