from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout
from page.ui.temperature_frame import TemperatureFrame
from page.utils.http_client import HttpClient


class TemperatureAction(QWidget):

    url = "http://192.168.1.103:7125/printer/gcode/script?include_monitors=false"

    temp = Signal(str)
    response = Signal(str)

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.temperature_frame = TemperatureFrame()
        self.init_layout()
        self.bind()


    def init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.temperature_frame)
        self.setLayout(layout)
    def bind(self):
        # self.timer.timeout.connect(self.update_temperature)
        self.temperature_frame.set_temperature_line_edit.returnPressed.connect(self.update_temperature)

    def update_temperature(self):
        temp = self.temperature_frame.set_temperature_line_edit.text()
        self.temp.emit(f"设置温度：{temp}℃")
        # print(f"设置温度：{temp}℃")
        res = HttpClient.extruder( url=self.url , script=f'SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET={temp}')
        self.response.emit(res)
