from PySide6.QtWidgets import QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel

from page.base.base_frame import BaseFrame


class MenuFrame(BaseFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def init_ui(self):
        self.robot_ip_label = QLabel("机器人IP地址：")
        self.robot_ip_line_edit = QLineEdit()
        self.robot_ip_line_edit.setPlaceholderText("请输入机械臂IP")
        self.open_file_btn = QPushButton("打开文件")
        self.open_file_name_label = QLabel()
        self.open_file_name_label.setMaximumSize(200, 30)
        self.power_on_btn = QPushButton("开机")
        self.power_off_btn = QPushButton("关机")
        self.start_btn = QPushButton("开始")
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("background-color: gray; color: black;")
        # self.start_btn.setDisabled(True)
        self.stop_btn = QPushButton("停止")
        self.pause_btn = QPushButton("暂停")
        self.resume_btn = QPushButton("恢复")
        self.restart_printer_btn = QPushButton("重启打印机")
        self.Gcode_input_edit = QLineEdit()
        self.Gcode_input_edit.setPlaceholderText("Gcode测试指令")
        self.Gcode_send_btn = QPushButton("发送Gcode")




    def init_layout(self):
        layout0 = QHBoxLayout()
        layout0.addWidget(self.robot_ip_label)
        layout0.addWidget(self.robot_ip_line_edit)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.open_file_btn)
        layout1.addWidget(self.open_file_name_label)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.start_btn)
        layout2.addWidget(self.stop_btn)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.pause_btn)
        layout3.addWidget(self.resume_btn)
        layout4 = QHBoxLayout()
        layout4.addWidget(self.restart_printer_btn)
        layout5 = QHBoxLayout()
        layout5.addWidget(self.power_on_btn)
        layout5.addWidget(self.power_off_btn)
        layout6 = QHBoxLayout()
        layout6.addWidget(self.Gcode_input_edit)
        layout7 = QHBoxLayout()
        layout7.addWidget(self.Gcode_send_btn)
        mainlayout  = QVBoxLayout(self)

        mainlayout.addLayout(layout0)
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout2)
        # mainlayout.addLayout(layout3)
        mainlayout.addLayout(layout4)
        # mainlayout.addLayout(layout5)
        mainlayout.addLayout(layout6)
        mainlayout.addLayout(layout7)
