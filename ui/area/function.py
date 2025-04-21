from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from ui.config import ConfigManager
from ui.widgets.expand_button import ExpandButton
from ui.widgets.avatar_selector import AvatarSelectorWidget

class FunctionArea(QWidget):
    insert_clicked = pyqtSignal(str, bool)  # text, is_me

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
        self.insert_btn = QPushButton("➕ 插入一条对话 😊")
        self.insert_btn.setFixedHeight(100)
        self.insert_btn.setFont(QFont("Microsoft YaHei", 11))
        self.insert_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px dashed #cccccc;
                border-radius: 12px;
                text-align: left;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e0ffe0;
                border-color: #07c160;
            }
        """)

        # 预留空间
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 添加布局项
        layout.addWidget(role_label)
        layout.addSpacing(10)  # 增加标题与头像间距
        layout.addWidget(self.avatar_selector)
        layout.addWidget(self.insert_btn)
        layout.addItem(spacer)

    def setup_connections(self):
        # 连接插入
        self.insert_btn.clicked.connect(self.insert_sample_message)

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/function.qss"))

    def insert_sample_message(self):
        text = "双击编辑对话 😊"
        is_me = self.avatar_selector.radio_me.isChecked()
        self.insert_clicked.emit(text, is_me)