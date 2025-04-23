from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal

class TitleWidget(QWidget):
    back_clicked = pyqtSignal()  # 返回按钮点击信号

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.init_ui()
        self.setup_events()

    def init_ui(self):
        self.setFixedHeight(44)
        self.setObjectName("TitleBar")  # 用于QSS选择器

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)

        # 返回按钮
        self.back_button = QLabel("⬅️")
        self.back_button.setObjectName("BackButton")
        layout.addWidget(self.back_button)

        # 可修改的标题（居中）
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label, stretch=1)  # 中间内容自动拉伸

        # 菜单按钮
        self.menu_button = QLabel("⋯")
        self.menu_button.setObjectName("MenuButton")
        layout.addWidget(self.menu_button, alignment=Qt.AlignRight)

    def setup_events(self):
        # 为返回按钮添加点击事件
        self.back_button.mousePressEvent = lambda _: self.back_clicked.emit()

    def set_title(self, text: str):
        """设置标题文本"""
        self.title_label.setText(text)
