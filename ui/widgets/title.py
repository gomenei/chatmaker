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

    def init_ui(self):
        self.setFixedHeight(50)  # 略高一点
        self.setObjectName("TitleBar")
        
        # 设置浅色背景
        self.setStyleSheet("""
            QWidget#TitleBar {
                background-color: #ededed;
                border-bottom: 1px solid #dbdbdb;
            }
            QLabel#BackButton {
                font-size: 20px;
                padding: 0 10px;
            }
            QLineEdit#TitleLabel {
                font-size: 17px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
            QLabel#MenuButton {
                font-size: 20px;
                padding: 0 10px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 返回按钮 - 使用微信样式的箭头
        self.back_button = QLabel()
        self.back_button.setObjectName("BackButton")
        self.back_button.setText("←")  # 更简洁的箭头
        self.back_button.setFixedWidth(40)  # 固定宽度
        layout.addWidget(self.back_button, alignment=Qt.AlignVCenter)

        # 标题 (居中)
        self.title_label = LineEditWidget(self.title)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label, stretch=1)

        # 菜单按钮 - 改为三个点垂直排列
        self.menu_button = QLabel("⋮")
        self.menu_button.setObjectName("MenuButton")
        self.menu_button.setFixedWidth(40)  # 固定宽度
        layout.addWidget(self.menu_button, alignment=Qt.AlignVCenter)

    def setup_events(self):
        self.back_button.mousePressEvent = lambda _: self.back_clicked.emit()

    def set_title(self, text: str):
        """设置标题文本"""
        self.title_label.setText(text)
