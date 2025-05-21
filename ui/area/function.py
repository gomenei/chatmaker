from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from ui.config import ConfigManager
from ui.widgets.expand_button import ExpandButton
from ui.widgets.avatar_selector import AvatarSelectorWidget

class FunctionArea(QWidget):
    insert_clicked = pyqtSignal(str, bool)  # text, is_me
    export_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # ==== 身份选择：头像 + 单选按钮 ====
        role_label = QLabel("Function")
        role_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        role_label.setAlignment(Qt.AlignCenter)  # 标题居中

        self.avatar_selector = AvatarSelectorWidget()

        # ==== 插入对话按钮 ====
        size = 120
        self.message_btn = ExpandButton("插入对话", [["文字消息", "语音消息", "语音通话"], ["视频通话", "图片消息", "表情包"]], (size * 2, size * 3))
        self.pocket_btn = ExpandButton("转账/红包", [["发送转账"], ["已被接收"], ["已收款"], ["发送红包"], ["已领取"]], (size, size * 5))
        self.time_btn = ExpandButton("插入时间", [["插入时间", "拍一拍"]], (size, 2 * size))
        self.other_btn = ExpandButton("更多功能", [["其他消息"]], (size, size))
        self.exit_btn = ExpandButton("退出", [[]], (0, 0))
        self.export_btn = ExpandButton("导出聊天记录", [[]], (240, 60))
        # 预留空间
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 添加布局项
        layout.addWidget(role_label)
        layout.addSpacing(10)  # 增加标题与头像间距
        layout.addWidget(self.avatar_selector)
        layout.addWidget(self.message_btn)
        layout.addWidget(self.pocket_btn)
        layout.addWidget(self.time_btn)
        layout.addWidget(self.other_btn)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.exit_btn)
        layout.addItem(spacer)

    def setup_connections(self):
        # 连接插入
        self.message_btn.button_clicked.connect(self.insert_sample_message)
        self.pocket_btn.button_clicked.connect(self.insert_sample_message)
        self.time_btn.button_clicked.connect(self.insert_sample_message)
        self.other_btn.button_clicked.connect(self.insert_sample_message)
        self.export_btn.clicked.connect(self.export_clicked.emit)
        self.exit_btn.clicked.connect(lambda: self.insert_sample_message("退出"))  # 退出按钮直接关闭窗口

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/function.qss"))

    def insert_sample_message(self, text):
        is_me = self.avatar_selector.radio_me.isChecked()
        self.insert_clicked.emit(text, is_me)