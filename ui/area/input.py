from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from ui.widgets.text_input import TextInput  # 单独的文本输入组件
from ui.config import ConfigManager

cfm = ConfigManager().instance()

class InputArea(QWidget):
    send_clicked = pyqtSignal()
    voice_clicked = pyqtSignal() #输入区域转换为语音输入
    emoji_clicked = pyqtSignal() #表情框弹出

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()
        self.load_style()

    def init_ui(self):
        width = self.parent().width()
        print("input width =", width)
        self.setFixedWidth(width)
        self.setFixedHeight(int(width * 0.14))
        icon_width = int(width / 90 * 7)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.voice_btn = QPushButton(self)
        self.voice_btn.setIconSize(QSize(icon_width, icon_width))
        #self.voice_icon = QIcon("./fig/icon/voice.jpg")
        self.voice_icon = QIcon(cfm.get_input_icon("voice"))
        self.voice_pressed_icon = QIcon(cfm.get_input_icon("voice_pressed"))
        self.voice_btn.setIcon(self.voice_icon)
        self.voice_btn.setStyleSheet("border: 1px solid red;")
        print("icon_width =", icon_width)

        self.emoji_btn = QPushButton(self)
        self.emoji_btn.setIconSize(QSize(icon_width, icon_width))
        self.emoji_icon = QIcon(cfm.get_input_icon("emoji"))
        self.emoji_pressed_icon = QIcon(cfm.get_input_icon("emoji_pressed"))
        self.emoji_btn.setIcon(self.emoji_icon)

        self.others_btn = QPushButton(self)
        self.others_btn.setIconSize(QSize(icon_width, icon_width))
        self.others_icon = QIcon(cfm.get_input_icon("others"))
        self.others_pressed_icon = QIcon(cfm.get_input_icon("others_pressed"))
        self.others_btn.setIcon(self.others_icon)

        self.input_box = TextInput(self)
        self.input_box.setStyleSheet("border: 1px solid red;")

        self.send_btn = QPushButton("发送")
        btn_width = int(0.1533 * width)
        self.send_btn.setFixedSize(
            btn_width,
            int (btn_width * 0.7)
        )
        print("send btn width = ", btn_width)
        print("send btn height = ", int(btn_width * 0.84))
        
        self.send_btn.setObjectName("send_btn")

        self.main_layout.addWidget(self.voice_btn, alignment=Qt.AlignBottom)
        self.main_layout.addWidget(self.input_box, alignment=Qt.AlignBottom)
        self.main_layout.addWidget(self.emoji_btn, alignment=Qt.AlignBottom)
        self.main_layout.addWidget(self.others_btn, alignment=Qt.AlignBottom)
        self.main_layout.addWidget(self.send_btn, alignment=Qt.AlignBottom)

        self.send_btn.hide()

    def setup_connections(self):
        # 连接按钮点击事件
        self.send_btn.clicked.connect(self.on_send_clicked)
        # Enter键快速发送
        self.input_box.send_trigger.connect(self.on_send_clicked)
        # 发送编辑事件
        self.emoji_btn.clicked.connect(lambda: self.emoji_clicked.emit())

        self.input_box.text_input.connect(self.non_null)
        self.voice_btn.pressed.connect(self.voice_pressed)
        self.voice_btn.released.connect(self.voice_released)
        self.emoji_btn.pressed.connect(self.emoji_pressed)
        self.emoji_btn.released.connect(self.emoji_released)
        self.others_btn.pressed.connect(self.others_pressed)
        self.others_btn.released.connect(self.others_released)

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

    def voice_pressed(self):
        self.voice_btn.setIcon(self.voice_pressed_icon)

    def voice_released(self):
        self.voice_btn.setIcon(self.voice_icon)

    def emoji_pressed(self):
        self.emoji_btn.setIcon(self.emoji_pressed_icon)

    def emoji_released(self):
        self.emoji_btn.setIcon(self.emoji_icon)

    def others_pressed(self):
        self.others_btn.setIcon(self.others_pressed_icon)

    def others_released(self):
        self.others_btn.setIcon(self.others_icon)