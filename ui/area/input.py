from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from ui.widgets.text_input import TextInput  # 单独的文本输入组件

class InputArea(QWidget):
    send_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()
        self.load_style()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.input_box = TextInput(self)
        self.send_btn = QPushButton("发送")

        self.main_layout.addWidget(self.input_box, alignment=Qt.AlignBottom)
        self.main_layout.addWidget(self.send_btn, alignment=Qt.AlignBottom)

    def setup_connections(self):
        # 连接按钮点击事件
        self.send_btn.clicked.connect(self.on_send_clicked)
        # Enter键快速发送
        self.input_box.send_trigger.connect(self.on_send_clicked)

    def on_send_clicked(self):
        """触发发送信号"""
        self.send_clicked.emit()

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/input.qss"))