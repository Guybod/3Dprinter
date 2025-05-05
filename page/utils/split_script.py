import time
import rtde_control
import rtde_receive
from threading import Thread
from PySide6.QtCore import QObject, Signal

class ScriptExecutor:
    def __init__(self, robot_ip, script_path, speed_ms=0.02, accel_mss=3.0, blend_radius_m=0.001, on_script_parsed=None):
        self.ROBOT_IP = robot_ip
        self.script_path = script_path
        self.speed_ms = speed_ms
        self.accel_mss = accel_mss
        self.blend_radius_m = blend_radius_m
        self.signal = True
        self.now_position = []

        self.rtde_c = rtde_control.RTDEControlInterface(self.ROBOT_IP)
        self.rtde_r = rtde_receive.RTDEReceiveInterface(self.ROBOT_IP)

        self.thread = Thread(target=self.print_position, daemon=True)
        self.parse_thread = None
        self.on_script_parsed = on_script_parsed

        self.signals = self.Signals()  # 初始化信号
        self.progress_thread = None  # 新增进度监控线程

    class Signals(QObject):
        log_message = Signal(str)
        operation_complete = Signal()

    def monitor_progress(self):
        Data = 0
        while self.signal:
            data = self.rtde_c.getAsyncOperationProgress()
            if Data != data:
                msg = f"当前进度: {data}"
                self.signals.log_message.emit(msg)
                Data = data
            if data < 0:
                self.signal = False
                self.signals.log_message.emit("脚本执行完成")
                self.signals.operation_complete.emit()
                break
            time.sleep(0.1)  # 控制频率避免 CPU 占用过高



    def print_position(self):
        while self.signal:
            try:
                self.now_position = self.rtde_r.getActualTCPPose()
                print(f"Current Position: {self.now_position}")
                time.sleep(0.05)
            except Exception as e:
                print(f"Position read error: {e}")
                break

    def parse_script(self):
        movement_dict = {}
        extruder_value = 0
        index = 1
        movepath = []

        with open(self.script_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('Extruder'):
                    extruder_value = float(line.split('(')[1].split(')')[0])
                elif line.startswith(('movej', 'movel')):
                    move_type = line.split('(')[0]
                    coords = line.split('[')[1].split(']')[0].split(',')
                    movepath = [float(c) for c in coords]

                    params = line.split('],')[1].split(')')[0].split(',')
                    if len(movepath) == 6:
                        movement_dict[index] = [move_type, movepath, *params, extruder_value]
                        movepath = []
                        index += 1
                        extruder_value = 0
        return movement_dict

    def run(self):
        if not self.rtde_c.isConnected():
            raise ConnectionError("无法连接到机械臂")

        print("机械臂已连接！")

        # 启动解析线程
        self.parse_thread = Thread(target=self.run_parse_in_thread, daemon=True)
        self.parse_thread.start()

        # 可以在这里先启动打印位置线程，或者等 parse 完成后启动
        self.thread.start()

        # 启动进度监控线程
        self.progress_thread = Thread(target=self.monitor_progress, daemon=True)
        self.progress_thread.start()
    def run_parse_in_thread(self):
        try:
            movement_dict = self.parse_script()
            if self.on_script_parsed:
                self.on_script_parsed(movement_dict)  # 解析完成后调用回调
        except Exception as e:
            print(f"解析脚本失败: {e}")
