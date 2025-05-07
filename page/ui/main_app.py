"""MainApp"""
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

from page.action.MenuFrameAction import MenuFrameAction
from page.action.TemperatureExtruderAction import TemperatureExtruderAction
from page.action.TemperatureHeaterBedAction import TemperatureHeaterBedAction
from page.action.TemperatureWorker import TemperatureWorker
from page.action.plainTextEditAction import PlainTextEditAction


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_layout()
        self.bind()


    def init_ui(self):
        self.temperature_heater_bed = TemperatureHeaterBedAction()
        self.temperature_extruder = TemperatureExtruderAction()
        self.log = PlainTextEditAction()
        self.temperature_worker = TemperatureWorker()
        self.worker_thread = QThread()
        self.temperature_worker.moveToThread(self.worker_thread)
        self.menu_frame = MenuFrameAction(self)


    def init_layout(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.center_layout = QHBoxLayout(self.central_widget)
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.temperature_heater_bed)
        self.left_layout.addWidget(self.temperature_extruder)
        self.left_layout.addWidget(self.log)
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.menu_frame)

        self.center_layout.addLayout(self.left_layout)
        self.center_layout.addLayout(self.right_layout)

    def bind(self):
        self.log.bind(self.temperature_heater_bed)
        self.log.bind(self.temperature_extruder)
        self.worker_thread.started.connect(self.temperature_worker.run)
        self.temperature_worker.temperature_updated.connect(self.update_temperature_labels)
        self.temperature_worker.temperature_updated.connect(self.check_temperature_threshold)

        # 监听温度设定值的变化
        self.temperature_heater_bed.temperature_frame.set_temperature_line_edit.textChanged.connect(
            self.check_temperature_threshold)
        self.temperature_extruder.temperature_frame.set_temperature_line_edit.textChanged.connect(
            self.check_temperature_threshold)

        self.worker_thread.start()
    def update_temperature_labels(self, temps):
        """
        接收温度列表 [extruder_temp, heater_bed_temp]
        并分别更新两个组件中的 current_temperature_label
        """
        if hasattr(self, 'temperature_extruder'):
            self.temperature_extruder.temperature_frame.current_temperature_label.setText(temps[0])
        if hasattr(self, 'temperature_heater_bed'):
            self.temperature_heater_bed.temperature_frame.current_temperature_label.setText(temps[1])

    def check_temperature_threshold(self, temps=None):
        """
        检查温度设定值和当前温度，决定是否启用开始按钮
        :param temps: 来自 temperature_updated 的实时温度列表 [extruder_temp, heater_bed_temp]
        """
        try:
            extruder_set = float(self.temperature_extruder.temperature_frame.set_temperature_line_edit.text() or 0)
            heater_bed_set = float(self.temperature_heater_bed.temperature_frame.set_temperature_line_edit.text() or 0)

            if temps is None:
                return

            extruder_current = float(temps[0].strip('℃'))
            heater_bed_current = float(temps[1].strip('℃'))

            if (extruder_set > 0 and heater_bed_set > 0 and
                    extruder_current >= extruder_set and heater_bed_current >= heater_bed_set):
                self.menu_frame.menu_frame.start_btn.setEnabled(True)
                self.menu_frame.menu_frame.start_btn.setStyleSheet("background-color: green; color: white;")
            else:
                self.menu_frame.menu_frame.start_btn.setEnabled(False)
                self.menu_frame.menu_frame.start_btn.setStyleSheet("background-color: gray; color: black;")

        except ValueError:
            pass  # 忽略非法输入