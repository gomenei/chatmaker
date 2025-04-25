from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt

class StatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(24)
        self.setStyleSheet("background-color: #ededed; color: black;")
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 确保背景覆盖

        self.status_layout = QHBoxLayout(self)
        self.status_layout.setContentsMargins(12, 0, 12, 0)

        # 左侧
        status_left = QLabel("🕛 12:30 | 📶 4G")
        self.status_layout.addWidget(status_left)

        # 中间 → 替换为 QLabel 使其可以填充背景
        status_middle = QLabel("")
        status_middle.setStyleSheet("background-color: #ededed;")
        self.status_layout.addWidget(status_middle, stretch=1)

        # 右侧
        status_right = QLabel("🔋 98% | 🔊")
        self.status_layout.addWidget(status_right)
