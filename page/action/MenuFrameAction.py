import time
from http.client import responses

from PySide6.QtWidgets import QWidget, QFileDialog, QVBoxLayout

from page.ui.menu_frame import MenuFrame
from page.utils.URDashboardClient import URDashboardClient
from page.utils.http_client import HttpClient
from page.utils.split_script import ScriptExecutor

import rtde_control

class MenuFrameAction(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.menu_frame = MenuFrame()
        self.init_layout()
        self.bind()
        self.file_name  = ""
        self.client = None

    def bind(self):
        self.menu_frame.open_file_btn.clicked.connect(self.open_file_btn_clicked)
        self.menu_frame.start_btn.clicked.connect(self.start_btn_clicked)
        self.menu_frame.stop_btn.clicked.connect(self.stop_btn_clicked)
        self.menu_frame.pause_btn.clicked.connect(self.pause_btn_clicked)
        self.menu_frame.resume_btn.clicked.connect(self.resume_btn_clicked)
        self.menu_frame.restart_printer_btn.clicked.connect(self.restart_printer_btn_clicked)
        self.menu_frame.Gcode_send_btn.clicked.connect(self.Gcode_send_btn_clicked)
        self.menu_frame.power_on_btn.clicked.connect(self.power_on_btn_clicked)
        self.menu_frame.power_off_btn.clicked.connect(self.power_off_btn_clicked)

    def init_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.menu_frame)
        self.setLayout(layout)

    def open_file_btn_clicked(self):
        """
                打开文件选择对话框。
                """
        # 调用 QFileDialog.getOpenFileName 方法打开文件选择对话框
        file_name, _ = QFileDialog.getOpenFileName(self.main_window, "选择文件", "", "Text Files (*.txt)")

        # 如果用户选择了文件，更新标签显示文件路径
        if file_name:
            name = file_name.split("/")[-1]
            self.menu_frame.open_file_name_label.setText(f"当前文件：{name}")
        self.file_name = file_name

    def create_client(self):
        if self.client:
            return
        elif self.menu_frame.robot_ip_line_edit.text():
            self.client = URDashboardClient(self.menu_frame.robot_ip_line_edit.text())

    def start_btn_clicked(self):
        if not self.file_name:
            self.main_window.log.update_text("请先选择一个脚本文件")
            return

        robot_ip = self.menu_frame.robot_ip_line_edit.text()
        if not robot_ip:
            self.main_window.log.update_text("请输入机械臂IP地址")
            return

        def on_script_parsed(movement_sites):
            print("脚本解析完成，开始执行路径...")

            path = rtde_control.Path()

            for key, value in movement_sites.items():
                pose = value[1]
                pose.append(self.executor.speed_ms)
                pose.append(self.executor.accel_mss)
                pose.append(
                    self.executor.blend_radius_m if value[4] == 'blend_radius_m' else self.executor.blend_radius_m)

                entry = rtde_control.PathEntry(rtde_control.PathEntry.MoveL, rtde_control.PathEntry.PositionTcpPose,
                                               pose)
                path.addEntry(entry)

            self.executor.rtde_c.moveL([0.009757, -0.460243, 0.121700, -0.000000, 3.141593, -0.000000],
                                       self.executor.speed_ms, self.executor.accel_mss)
            self.executor.rtde_c.movePath(path, asynchronous=False)

            Data = 0
            while self.executor.signal:
                data = self.executor.rtde_c.getAsyncOperationProgress()
                if Data != data:
                    print(data)
                    Data = data
                if data < 0:
                    self.executor.signal = False
                    self.executor.thread.join()
                    break

            time.sleep(1)
            new_position = self.executor.now_position
            new_position[2] += 0.05
            self.executor.rtde_c.moveL(new_position, self.executor.speed_ms, self.executor.accel_mss)
            self.main_window.log.update_text("脚本执行完成")

        try:
            # 创建 ScriptExecutor 并传入回调
            self.executor = ScriptExecutor(robot_ip=robot_ip, script_path=self.file_name,
                                           on_script_parsed=on_script_parsed)

            # 连接信号
            self.executor.signals.log_message.connect(lambda msg: self.main_window.log.update_text(msg))
            self.executor.signals.operation_complete.connect(lambda: self.main_window.log.update_text("脚本执行完成"))

            self.executor.run()
            self.main_window.log.update_text("脚本正在运行")
        except Exception as e:
            self.main_window.log.update_text(f"执行失败: {str(e)}")

    def stop_btn_clicked(self):
        if self.client:
            res = self.client.send_command("pause")
            self.main_window.log.update_text(res)
            res = self.client.send_command("stop")
            self.main_window.log.update_text(res)
            self.main_window.log.update_text("机械臂已停止")
        elif self.menu_frame.robot_ip_line_edit.text():
            self.client = URDashboardClient(self.menu_frame.robot_ip_line_edit.text())
            res = self.client.send_command("pause")
            self.main_window.log.update_text(res)
            res = self.client.send_command("stop")
            self.main_window.log.update_text(res)
            self.main_window.log.update_text("机械臂已停止")
        else:
            self.main_window.log.update_text("请输入机械臂IP")

    def pause_btn_clicked(self):
        pass

    def resume_btn_clicked(self):
        pass

    def power_on_btn_clicked(self):
        pass

    def power_off_btn_clicked(self):
        pass

    def restart_printer_btn_clicked(self):
        # response1 = HttpClient.POST("http://192.168.1.103:7125/printer/firmware_restart", "")
        # response2 = HttpClient.POST("http://192.168.1.103:7125/printer/restart", "")
        #
        # self.main_window.log.update_text(f"{response1.text}")
        # time.sleep(1)
        # self.main_window.log.update_text(f"{response2.text}")
        # time.sleep(0.5)
        # self.main_window.log.update_text("重启打印机")
        pass
    def Gcode_send_btn_clicked(self):
        script = self.menu_frame.Gcode_input_edit.text()
        response = HttpClient.POST("http://192.168.1.103:7125/printer/gcode/script?include_monitors=false", script)
        if response.status_code == 200:
            self.main_window.log.update_text(f"{script} 发送成功")
        else:
            self.main_window.log.update_text("发送失败")


