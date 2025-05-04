# TemperatureAction.py
from PySide6.QtCore import QObject, QThread, Signal

from page.utils.http_client import HttpClient

url = "http://192.168.1.103:7125/printer/gcode/script?include_monitors=false"


class TemperatureWorker(QObject):
    temperature_updated = Signal(str)  # 自定义信号，用于更新温度

    def __init__(self):
        super().__init__()
        self.is_running = True
    def run(self):
        while self.is_running:
            # 模拟获取温度数据
            temp = self.get_temperature_from_device()
            self.temperature_updated.emit(temp)
            QThread.msleep(500)  # 每秒查询一次

    def get_temperature_from_device(self):
        HttpClient.extruder(f"SET")
        return "25°C"
