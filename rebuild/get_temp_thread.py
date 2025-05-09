import requests
from PySide6.QtCore import QThread, Signal
from read_config import get_config

class TempCollectorThread(QThread):
    """
    数据收集线程
    """
    temp_collected = Signal(list)  # 自定义信号，用于将数据发送回主线程

    def __init__(self):
        super().__init__()
        self.ROBOT_IP = get_config("ROBOT_IP")
        self.WEB_IP = get_config("WEB_IP")
        self.TIME_SLEEP = get_config("TIME_SLEEP")


    def run(self):
        """
        数据收集的死循环
        """
        while True:
            # 模拟数据收集
            data = self.collect_temp()
            self.temp_collected.emit(data)  # 发射数据
            QThread.msleep(int(self.TIME_SLEEP))

    def collect_temp(self):
        url = f"http://{self.WEB_IP}:7125/server/temperature_store?include_monitors=true"

        payload={}
        headers = {
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Accept': '*/*',
           'Host': f'{self.WEB_IP}:7125',
           'Connection': 'keep-alive'
        }

        try:
            response = requests.request("GET", url, headers=headers, data=payload)

            data = response.json()

            extruder_temperatures = data["result"]["extruder"]["temperatures"]
            header_bed_temperatures = data["result"]["heater_bed"]["temperatures"]

            return [extruder_temperatures[-1],header_bed_temperatures[-1]]
        except Exception as e:
            print(e)
            return [0,0]