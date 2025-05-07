import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from rebuild.get_temp_thread import TempCollectorThread
from rebuild.main_window_app import MainApp


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainApp()  # 创建 Page 对象
        self.ui.setFixedSize(500, 600)
        self.setCentralWidget(self.ui)
        self.relay_time_temp = TempCollectorThread()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainForm()
    main_window.show()
    sys.exit(app.exec())
