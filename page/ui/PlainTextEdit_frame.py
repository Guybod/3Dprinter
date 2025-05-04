from PySide6.QtWidgets import QPlainTextEdit, QHBoxLayout

from page.base.base_frame import BaseFrame


class PlainTextEditFrame(BaseFrame):

    def __init__(self):
        super().__init__()
        self.log_text = None
        self.setup_ui()

    def init_ui(self):
        self.log_text = QPlainTextEdit()

    def init_layout(self):
        layout = QHBoxLayout(self)
        layout.addWidget(self.log_text)
