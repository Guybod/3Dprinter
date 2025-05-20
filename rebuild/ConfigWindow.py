from PySide6.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QPushButton


class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置文件编辑")
        self.resize(500, 400)

        self.layout = QVBoxLayout(self)

        self.config_text_edit = QPlainTextEdit(self)
        self.layout.addWidget(self.config_text_edit)

        self.save_button = QPushButton("保存", self)
        self.layout.addWidget(self.save_button)

    def set_config_content(self, content):
        self.config_text_edit.setPlainText(content)

    def get_config_content(self):
        return self.config_text_edit.toPlainText()
