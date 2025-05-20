"""MainApp"""
from PySide6.QtCore import Slot, QThreadPool
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from rebuild.ConfigWindow import ConfigWindow
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
        self.thread_pool.setMaxThreadCount(10)

    def init_ui(self):
        pass

    def init_layout(self):
        self.setCentralWidget(self.central_widget)
        self.center_layout = QHBoxLayout(self.central_widget)

    def bind(self):
        self.central_widget.start_btn.clicked.connect(self.on_start_btn)
        self.central_widget.config_btn.clicked.connect(self.open_config)
        self.central_widget.pause_btn.clicked.connect(self.on_pause_btn)
        self.central_widget.stop_btn.clicked.connect(self.on_stop_bth)
        self.central_widget.Dashbord_Send_btn.clicked.connect(self.send_dashbord_command)

    def on_start_btn(self):
        worker = Worker("split_script",'script.txt')
        worker.signals.result_ready.connect(self.display_result)
        self.thread_pool.start(worker)
        self.central_widget.log_text_edit.appendPlainText("开始执行")

    @Slot(object)
    def display_result(self, result):
        self.central_widget.log_text_edit.appendPlainText(f"{result}")


    @Slot(object)
    def display_data(self, data):
        """
        在主线程中显示数据
        """
        self.central_widget.extruder_temp_label.setText(f"挤出温度：  {data[0]}℃ /")
        self.central_widget.heater_bed_temp_label.setText(f"热床温度   : {data[0]}℃ /")

    def open_config(self):
        try:
            with open("config.cfg", "r", encoding='utf-8') as file:
                config_content = file.read()

            self.config_window = ConfigWindow(self)
            self.config_window.set_config_content(config_content)
            self.config_window.save_button.clicked.connect(lambda: self.save_config_from_window(self.config_window))
            self.config_window.exec()  # 使用模态对话框
        except Exception as e:
            self.central_widget.log_text_edit.appendPlainText(f"读取配置文件失败: {str(e)}")

    def save_config_from_window(self, window):
        config_content = window.get_config_content()
        try:
            with open("config.cfg", "w", encoding='utf-8') as file:
                file.write(config_content)
            self.central_widget.log_text_edit.appendPlainText("配置文件保存成功")
            window.accept()  # 关闭窗口
        except Exception as e:
            self.central_widget.log_text_edit.appendPlainText(f"保存配置文件失败: {str(e)}")

    def on_pause_btn(self):
        worker_disconnect = Worker("disconnect")
        worker_disconnect.signals.result_ready.connect(lambda _: self.send_dashbord_command("pause"))
        self.thread_pool.start(worker_disconnect)

    def on_stop_bth(self):
        worker_disconnect = Worker("disconnect")
        worker_disconnect.signals.result_ready.connect(lambda _: self.send_dashbord_command("stop"))
        self.thread_pool.start(worker_disconnect)

    def send_dashbord_command(self, cmd):
        if self.central_widget.Dashbord_edit.text() == "":
            worker = Worker("Dashbord", cmd)
            worker.signals.result_ready.connect(self.display_result)
            self.thread_pool.start(worker)
        else:
            worker = Worker("Dashbord", self.central_widget.Dashbord_edit.text())
            worker.signals.result_ready.connect(self.display_result)
            self.thread_pool.start(worker)

