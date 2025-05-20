import sys
import time
import ctypes
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QProcess, QTimer
from PySide6.QtGui import QWindow

# Windows API函数
user32 = ctypes.windll.user32
FindWindowW = user32.FindWindowW
FindWindowExW = user32.FindWindowExW
SetParent = user32.SetParent
ShowWindow = user32.ShowWindow
SW_SHOW = 5


def find_window_by_pid(pid):
    target_hwnd = None  # 修改外层变量名避免冲突

    def enum_proc(hWnd, lParam):
        nonlocal target_hwnd  # 现在引用外层作用域的变量
        lpdw_pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hWnd, ctypes.byref(lpdw_pid))
        if lpdw_pid.value == lParam:
            target_hwnd = hWnd  # 将找到的句柄赋值给外层变量
            return False  # 停止枚举
        return True  # 继续枚举

    # 修正回调函数类型定义
    enum_callback = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))(enum_proc)
    user32.EnumWindows(enum_callback, pid)
    return target_hwnd


class EmbedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口嵌入示例")
        self.layout = QVBoxLayout(self)

        self.btn_start = QPushButton("启动记事本并嵌入")
        self.btn_start.clicked.connect(self.start_exe)
        self.layout.addWidget(self.btn_start)

        self.process = QProcess()
        self.target_hwnd = None

    def start_exe(self):
        self.process.start("notepad.exe")
        if not self.process.waitForStarted():
            print("启动失败")
            return

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.check_window(self.process.processId()))
        self.timer.start(500)

    def check_window(self, pid):
        self.target_hwnd = find_window_by_pid(pid)
        if self.target_hwnd:
            self.timer.stop()
            self.embed_window()

    def embed_window(self):
        if not self.target_hwnd:
            return

        # 将外部窗口设置为当前QWidget的子窗口
        SetParent(self.target_hwnd, int(self.winId()))

        # 创建QWindow并包装为QWidget
        foreign_window = QWindow.fromWinId(self.target_hwnd)
        container = self.createWindowContainer(foreign_window, self)
        self.layout.addWidget(container)

        # 显示窗口
        ShowWindow(self.target_hwnd, SW_SHOW)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmbedWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())