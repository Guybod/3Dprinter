"""MainForm"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from page.ui.main_app import MainApp


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainApp()  # 创建 Page 对象
        self.setCentralWidget(self.ui)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainForm()
    main_window.show()
    sys.exit(app.exec())
