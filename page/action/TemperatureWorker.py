# TemperatureHeaterBedAction.py
import requests
from PySide6.QtCore import QObject, QThread, Signal

class TemperatureWorker(QObject):
    temperature_updated = Signal(list)  # 自定义信号，用于更新温度

    def __init__(self):
        super().__init__()
        self.is_running = True
    def run(self):
        while self.is_running:
            try:
                # 模拟获取温度数据
                temp = self.get_temperature()
                self.temperature_updated.emit(temp)

            except Exception as e:
                print(f"Error: {e}")
            QThread.msleep(500)  # 每秒查询一次

    def get_temperature(self):
        url = "http://192.168.1.103:7125/server/temperature_store?include_monitors=true"

        payload={}
        headers = {
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Accept': '*/*',
           'Host': '192.168.1.103:7125',
           'Connection': 'keep-alive'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()

        extruder_temperatures = data["result"]["extruder"]["temperatures"]
        header_bed_temperatures = data["result"]["heater_bed"]["temperatures"]

        return [str(extruder_temperatures[-1]) + '℃',
                str(header_bed_temperatures[-1]) + '℃']