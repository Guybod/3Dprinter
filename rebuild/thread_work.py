import json

import requests
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from rebuild.read_config import get_config

from http_utils import HttpClient

class Worker(QRunnable):

    class Signals(QObject):
        result_ready = Signal(object)

    def __init__(self, task_name, *args, **kwargs):
        super().__init__()
        self.task_name = task_name
        self.args = args  # 位置参数，存储在元组中
        self.kwargs = kwargs  # 关键字参数，存储在字典中
        self.WEB_IP = get_config("WEB_IP")
        self.signals = self.Signals()


    @Slot()
    def run(self):
        """
        Your long-running task goes here
        """
        if self.task_name == "send_script":
            result = self.send_script(self.args[0])  # 使用位置参数
        elif self.task_name == "demo":
            result = HttpClient.demo()
        elif self.task_name == "reverse_string":
            result = self.args[0][::-1]  # 使用位置参数
        elif self.task_name == "greet":
            result = f"Hello, {self.kwargs.get('name', 'Guest')}!"  # 使用关键字参数
        else:
            result = "Unknown task"
        self.signals.result_ready.emit(result)  # 将结果发送回主线程

    def send_script(self,script):
        url = f"http://{self.WEB_IP}:7125/printer/gcode/script?include_monitors=false"

        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': f'{self.WEB_IP}:7125',
            'Connection': 'keep-alive'
        }

        payload = json.dumps({
            "script": script
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        return response