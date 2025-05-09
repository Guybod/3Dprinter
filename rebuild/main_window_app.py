"""MainApp"""
from PySide6.QtCore import Slot, QThreadPool
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from rebuild.get_temp_thread import TempCollectorThread
from rebuild.main_window_ui import MainWindowUI
from rebuild.thread_work import Worker


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = MainWindowUI()
        self.init_ui()
        self.init_layout()
        self.bind()
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(5)
        self.temperature_thread = TempCollectorThread()

    def init_ui(self):
        pass

    def init_layout(self):
        self.setCentralWidget(self.central_widget)
        self.center_layout = QHBoxLayout(self.central_widget)

    def bind(self):
        self.central_widget.start_btn.clicked.connect(self.start_task_thread)
        self.central_widget.begin_btn.clicked.connect(self.start_temp_collector)
        self.temperature_thread.temp_collected.connect(self.display_data)

    def start_task_thread(self):
        worker = Worker("demo")
        worker.signals.result_ready.connect(self.display_result)
        self.thread_pool.start(worker)

    @Slot(object)
    def display_result(self, result):
        self.central_widget.log_text_edit.appendPlainText(f"{result}")


    @Slot(object)
    def display_data(self, data):
        """
        在主线程中显示数据
        """
        self.central_widget.extruder_temp_label.setText(f"挤出温度：  {data[0]}℃ /")
        self.central_widget.heater_bed_temp_label.setText(f"热床温度   : {data[1]}℃ /")

    def start_temp_collector(self):
        if not self.temperature_thread.isRunning():
            self.temperature_thread.start()