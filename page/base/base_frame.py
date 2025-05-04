"""base_frame.py"""

from abc import abstractmethod

from PySide6.QtWidgets import QFrame, QHBoxLayout


class BaseFrame(QFrame):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        self.init_ui()
        self.init_layout()


    @abstractmethod
    def init_ui(self):
        pass

    @abstractmethod
    def init_layout(self):
        layout = QHBoxLayout(self)
        self.setLayout(layout)

    def set_style(self):
        pass

    def bind(self):
        pass

    def show_box(self):
        self.setFrameShape(QFrame.Shape.Box)

    def hide_box(self):
        pass