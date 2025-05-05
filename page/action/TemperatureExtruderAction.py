from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout
from page.ui.temperature_frame import TemperatureFrame
from page.utils.http_client import HttpClient


class TemperatureExtruderAction(QWidget):

    url = "http://192.168.1.103:7125/printer/gcode/script?include_monitors=false"

    temp = Signal(str)
    # response = Signal(str)

    def __init__(self):
        super().__init__()
        self.temperature_frame = TemperatureFrame("挤出温度：")
        self.init_layout()
        self.bind()


    def init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.temperature_frame)
        self.setLayout(layout)
    def bind(self):
        # self.timer.timeout.connect(self.update_temperature)
        self.temperature_frame.set_temperature_line_edit.returnPressed.connect(self.update_temperature_extruder)

    def update_temperature_extruder(self):
        temp = self.temperature_frame.set_temperature_line_edit.text()
        self.temp.emit(f"设置挤出温度：{temp}℃")
        # print(f"设置温度：{temp}℃")
        res = HttpClient.POST( url=self.url , script=f'SET_HEATER_TEMPERATURE HEATER=extruder TARGET={temp}')
        res.json()
        if res.status_code == 200:
            self.temp.emit("挤出温度设置成功")
        # print(res)
        # self.response.emit(res)
