import json

import requests
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from rebuild.read_config import get_config

from http_utils import HttpClient
import rtde_control

class Worker(QRunnable):

    class Signals(QObject):
        result_ready = Signal(object)
        path = Signal(object)

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
        elif self.task_name == "split_script":
            path = self.args[0]
            self.signals.path.emit(path)
            result = "路径解析完毕"
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

    def split_script(self,script_path):
        # 用于存储最终结果的字典，键为递增数字，值为包含移动指令、参数和挤出机值的列表
        movement_dict = {}
        # 用于记录Extruder后面的值，初始化为0
        extruder_value = 0
        # 用于生成递增的数字键，初始化为1
        index = 1
        movepath = []

        speed_ms = 0.02
        accel_mss = 3.0
        blend_radius_m = 0.002

        path = rtde_control.Path()

        with open(script_path, 'r') as file:
            # 读取文件的所有行
            lines = file.readlines()
            for i in range(len(lines)):
                # 去除每行两端的空白字符
                line = lines[i].strip()
                if line.startswith('Extruder'):
                    # 提取Extruder括号内的值并转换为浮点数，赋值给extruder_value
                    extruder_value = float(line.split('(')[1].split(')')[0])
                elif line.startswith('movej') or line.startswith('movel'):
                    move_type = line.split('(')[0]
                    # 提取movej或movel括号内的参数内容
                    for i in line.split('[')[1].split(']')[0].split(','):
                        movepath.append(float(i))
                    move_parameter_0 = line.split('],')[1].split(')')[0].split(',')[0]
                    move_parameter_1 = line.split('],')[1].split(')')[0].split(',')[1]
                    move_parameter_2 = line.split('],')[1].split(')')[0].split(',')[2]
                    move_parameter_3 = line.split('],')[1].split(')')[0].split(',')[3]
                    if len(movepath) == 6:
                        movement_dict[index] = [move_type, movepath, move_parameter_0, move_parameter_1,
                                                move_parameter_2, move_parameter_3, extruder_value]
                        movepath = []
                    index += 1
                    extruder_value = 0
                elif line.startswith('speed_ms'):
                    continue


        for key, value in movement_dict.items():
            # print(key, value)
            pose = value[1]  # 当前位姿 [x, y, z, rx, ry, rz]

            pose.append(speed_ms)
            pose.append(accel_mss)

            if value[4] == 'blend_radius_m':
                pose.append(blend_radius_m)
            else:
                pose.append(blend_radius_m)

            entry = rtde_control.PathEntry(rtde_control.PathEntry.MoveL, rtde_control.PathEntry.PositionTcpPose, pose)
            path.addEntry(entry)

        return path