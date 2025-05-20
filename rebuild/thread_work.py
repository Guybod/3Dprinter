import time

import requests, socket, json, rtde_control
from PySide6.QtCore import QRunnable, Signal, Slot, QObject
from rebuild.read_config import get_config
from split_path import split_script
from threading import Lock, Thread
from PySide6.QtCore import QTimer

class Worker(QRunnable):
    # 定义一个类级锁，用于保护 RTDEControlInterface 的访问
    _rtde_lock = Lock()

    class Signals(QObject):
        result_ready = Signal(object)
        path = Signal(object)
        tip = Signal(str)

    def __init__(self, task_name, *args, **kwargs):
        super().__init__()
        self.task_name = task_name
        self.args = args  # 位置参数，存储在元组中
        self.kwargs = kwargs  # 关键字参数，存储在字典中
        self.ROBOT_IP = get_config("ROBOT_IP").strip()  # 去除首尾空格/换行
        self.WEB_IP = get_config("WEB_IP").strip()  # 去除首尾空格/换行
        self.signals = self.Signals()
        self.rtde_c = None
        self.speed_ms = get_config("SPEED_MS").strip()  # 去除首尾空格/换行
        self.accel_mss = get_config("ACCEL_MS").strip()  # 去除首尾空格/换行
        self.blend_radius_m = get_config("BLEND_RADIUS_M").strip()  # 去除首尾空格/换行

    @Slot()
    def run(self):
        """
        Your long-running task goes here
        """
        if self.task_name == "send_script":
            self.signals.result_ready.emit("send_script")
        elif self.task_name == "disconnect":
            if self.rtde_c is not None:
                try:
                    self.rtde_c.disconnect()
                    self.rtde_c = None
                    self.signals.result_ready.emit("RTDE 连接已断开")
                except Exception as e:
                    self.signals.result_ready.emit(f"断开 RTDE 连接失败: {str(e)}")
            else:
                self.signals.result_ready.emit("当前无 RTDE 连接")

        elif self.task_name == "split_script":
            # 确保只有一个线程可以进入 RTDE 初始化区域
            with Worker._rtde_lock:
                # 如果已有连接，先断开并释放
                if self.rtde_c is not None:
                    try:
                        self.rtde_c.disconnect()
                    except Exception as e:
                        self.signals.result_ready.emit(f"清理旧连接失败: {str(e)}")
                    finally:
                        self.rtde_c = None

                try:
                    # 创建新的 RTDEControlInterface 实例
                    self.rtde_c = rtde_control.RTDEControlInterface(self.ROBOT_IP)
                except Exception as e:
                    self.signals.result_ready.emit(f"无法创建 RTDEControlInterface: {str(e)}")
                    return
            path_file = self.args[0]
            dict = split_script(path_file)
            path = rtde_control.Path()

            for key, value in dict.items():
                # print(key, value)
                pose = value[1]  # 当前位姿 [x, y, z, rx, ry, rz]

                pose.append(float(self.speed_ms))
                pose.append(float(self.accel_mss))

                if value[4] == 'blend_radius_m':
                    pose.append(float(self.blend_radius_m))
                else:
                    pose.append(float(self.blend_radius_m))

                entry = rtde_control.PathEntry(rtde_control.PathEntry.MoveL, rtde_control.PathEntry.PositionTcpPose,
                                               pose)
                path.addEntry(entry)

            self.rtde_c.movePath(path, asynchronous=True)

            self.signals.result_ready.emit("路径解析完毕，启动机械臂")

            # Thread(target=self.polling_loop, daemon=True).start()

        elif self.task_name == "Dashbord":
            if self.rtde_c is not None:
                try:
                    self.rtde_c.disconnect()
                    self.rtde_c = None
                    self.signals.result_ready.emit("RTDE 连接已断开")
                except Exception as e:
                    self.signals.result_ready.emit(f"断开 RTDE 失败: {str(e)}")
            else:
                self.signals.result_ready.emit("当前无 RTDE 连接")
            cmd = self.args[0]
            robot_ip = self.ROBOT_IP
            port = 29999  # 指定端口号

            try:
                # 创建socket连接
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((robot_ip, port))  # 连接到指定IP和端口
                    s.sendall((cmd + '\n').encode())  # 发送带换行的命令
                    self.signals.result_ready.emit(f"命令 [{cmd}] 命令已发送")

            except Exception as e:
                self.signals.result_ready.emit(f"发送[{cmd}]命令失败: {str(e)}")
        else:
            result = "Unknown task"
            self.signals.result_ready.emit(result)  # 将结果发送回主线程


    def polling_loop(self):
        Data = 0
        Signal_= True
        while Signal_:
            data = self.rtde_c.getAsyncOperationProgress()
            if Data != data:
                # extruder("G1 E10 F300")
                print(Data)
                self.signals.result_ready.emit(data)
                Data = data
            if data < 0:
                Signal_ = False
                self.rtde_c = None
                break
            time.sleep(0.01)  # 每隔 50ms 查询一次

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
