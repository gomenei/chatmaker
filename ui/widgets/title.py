from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from ui.widgets.line_edit import LineEditWidget

class TitleWidget(QWidget):
    back_clicked = pyqtSignal()  # 返回按钮点击信号

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.init_ui()
        self.setup_events()
        self.load_style()

    def init_ui(self):
        self.setFixedHeight(50)  # 略高一点
        self.setObjectName("TitleWidget")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 返回按钮 - 使用微信样式的箭头

        self.back_button = QLabel()
        self.back_button.setObjectName("BackButton")
        self.back_button.setText("<")  # 更简洁的箭头
        # self.back_button.setFixedWidth(40)  # 固定宽度
        self.unread_bubble = LineEditWidget("99+")
        self.unread_bubble.setObjectName("UnreadBubble")
        self.unread_bubble.setAlignment(Qt.AlignRight)

        back_container = QWidget()
        back_layout = QHBoxLayout(back_container)
        back_layout.setContentsMargins(0, 0, 0, 0)  # 消除默认边距
        back_layout.setSpacing(2)  # 设置组件间距为2px
        back_layout.addWidget(self.back_button)
        back_layout.addWidget(self.unread_bubble)
        layout.addWidget(back_container, alignment=Qt.AlignLeft)

        # 标题 (居中)
        self.title_container = QWidget()
        title_layout = QHBoxLayout(self.title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = LineEditWidget(self.title, self)
        self.title_label.setText("微信聊天")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.title_container, stretch=1)

        # 菜单按钮
        self.menu_button = QLabel("⋯")
        self.menu_button.setObjectName("MenuButton")
        self.menu_button.setFixedWidth(40)  # 固定宽度
        layout.addWidget(self.menu_button, alignment=Qt.AlignRight)

    def setup_events(self):
        self.back_button.mousePressEvent = lambda _: self.back_clicked.emit()

    def set_title(self, text: str):
        """设置标题文本"""
        self.title_label.setText(text)

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/title.qss"))
