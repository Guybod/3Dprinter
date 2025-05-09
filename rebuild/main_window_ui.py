from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QFrame, QPlainTextEdit, QLineEdit, QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout

class MainWindowUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.init_ui()
        self.init_layout()
        self.setup_style()

    def init_ui(self):
        self.left_frame = QFrame()
        self.right_frame = QFrame()
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.left_frame)
        self.layout().addWidget(self.right_frame)

        self.log_text_edit = QPlainTextEdit()
        self.extruder_temp_label = QLabel("挤出温度：  - ℃ /")
        self.heater_bed_temp_label = QLabel("热床温度：  - ℃ /")
        self.extruder_temp_edit = QLineEdit()
        self.heater_bed_temp_edit = QLineEdit()
        self.begin_btn = QPushButton("开始")
        self.start_btn = QPushButton("启动")
        self.Gcode_edit = QLineEdit()
        self.Gcode_edit.setPlaceholderText("在此输入GCode")
        self.Gcode_Send_btn = QPushButton("发送")


    def init_layout(self):
        self.setLayout(QHBoxLayout())

        self.left_layout = QVBoxLayout()
        self.left_frame.setLayout(self.left_layout)
        layout1 = QHBoxLayout()
        layout1.addStretch(1)  # 添加伸展空间
        layout1.addWidget(self.extruder_temp_label)
        layout1.addWidget(self.extruder_temp_edit)
        layout1.addStretch(1)  # 添加伸展空间

        layout2 = QHBoxLayout()
        layout2.addStretch(1)  # 添加伸展空间
        layout2.addWidget(self.heater_bed_temp_label)
        layout2.addWidget(self.heater_bed_temp_edit)
        layout2.addStretch(1)  # 添加伸展空间

        self.left_layout.addLayout(layout1)
        self.left_layout.addLayout(layout2)
        self.left_layout.addWidget(self.log_text_edit)

        self.right_layout = QVBoxLayout()
        self.right_frame.setLayout(self.right_layout)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.begin_btn)
        layout3.addWidget(self.start_btn)
        layout4 = QHBoxLayout()
        layout4.addWidget(self.Gcode_edit)
        layout5 = QHBoxLayout()
        layout5.addWidget(self.Gcode_Send_btn)
        self.right_layout.addLayout(layout3)
        self.right_layout.addLayout(layout4)
        self.right_layout.addLayout(layout5)


    def setup_style(self):
        self.setStyleSheet("""
        QLineEdit {
            border: none;
            background-color: white;
            color: black;
        }
        """)
        self.extruder_temp_edit.setFixedWidth(50)
        self.heater_bed_temp_edit.setFixedWidth(50)

        # 设置验证器，限制输入范围为 -325 到 500
        validator = QIntValidator(-325, 500)
        self.extruder_temp_edit.setValidator(validator)
        self.heater_bed_temp_edit.setValidator(validator)
