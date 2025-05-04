from PySide6.QtWidgets import QWidget, QVBoxLayout
from page.ui.PlainTextEdit_frame import PlainTextEditFrame

class PlainTextEditAction(QWidget):
    def __init__(self):
        super().__init__()
        self.plain_text_edit = PlainTextEditFrame()        
        self.init_layout()

    def init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.plain_text_edit)
        self.setLayout(layout)

    def bind(self, temperature_action):
        temperature_action.temp.connect(self.update_text)

    def update_text(self, message):
        self.plain_text_edit.log_text.appendPlainText(message)

