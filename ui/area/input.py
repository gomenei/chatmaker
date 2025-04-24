from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from ui.widgets.text_input import TextInput  # 单独的文本输入组件

class InputArea(QWidget):
    send_clicked = pyqtSignal()
    voice_clicked = pyqtSignal() #输入区域转换为语音输入

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()
        self.load_style()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.voice_btn = QPushButton(self)
        self.voice_btn.setIcon(QIcon("./fig/icon/voice.jpg"))
        self.voice_btn.setIconSize(QSize(30, 30))

        self.emoji_btn = QPushButton(self)
        self.emoji_btn.setIcon(QIcon("./fig/icon/emoji.jpg"))
        self.emoji_btn.setIconSize(QSize(30, 30))

        self.others_btn = QPushButton(self)
        self.others_btn.setIcon(QIcon("./fig/icon/others.jpg"))
        self.others_btn.setIconSize(QSize(30, 30))

        self.input_box = TextInput(self)
        self.send_btn = QPushButton("发送")
        self.send_btn.setObjectName("send_btn")

        self.main_layout.addWidget(self.voice_btn, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.input_box, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.emoji_btn, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.others_btn, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.send_btn, alignment=Qt.AlignCenter)

        self.send_btn.hide()

    def setup_connections(self):
        # 连接按钮点击事件
        self.send_btn.clicked.connect(self.on_send_clicked)
        # Enter键快速发送
        self.input_box.send_trigger.connect(self.on_send_clicked)

        self.input_box.text_input.connect(self.non_null)

    def on_send_clicked(self):
        """触发发送信号"""
        self.send_clicked.emit()

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/input.qss"))

    def non_null(self, nonnull):
        if nonnull:
            self.others_btn.hide()
            self.send_btn.show()
        else:
            self.send_btn.hide()
            self.others_btn.show()