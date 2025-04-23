from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt, QPropertyAnimation, QEasingCurve, QEvent
from PyQt5.QtGui import QPixmap, QMouseEvent
from ui.config import ConfigManager

class InsertButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text, icon_path):
        super().__init__()
        self.text = text

        self.icon_path = ConfigManager().instance().get_icon_path(text)
        self.init_ui()
        self.load_style()

    def init_ui(self):
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)     # 改善鼠标跟踪
        self.setMaximumSize(100, 100)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)

        # 图标
        self.icon = QLabel()
        self.icon.setObjectName("icon")
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setPixmap(QPixmap(self.icon_path).scaled(100, 80, Qt.KeepAspectRatio))
        self.icon.setAutoFillBackground(False)

        # 文本
        self.label = QLabel(self.text)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setAutoFillBackground(False)

        # 添加到布局
        layout.addWidget(self.icon)
        layout.addWidget(self.label)

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/insert_button.qss"))

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.setProperty("press", "true")
            self.setGeometry(self.x() + 5, self.y() + 5, self.width(), self.height())
            self.label.style().polish(self.label)
            self.icon.style().polish(self.icon)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.setProperty("press", "false")
            self.setGeometry(self.x() - 5, self.y() - 5, self.width(), self.height())
            self.label.style().polish(self.label)
            self.icon.style().polish(self.icon)

            if self.rect().contains(event.pos()):
                self.clicked.emit()
                event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def enterEvent(self, event):
        """鼠标进入事件 - 悬停效果在样式表中实现"""
        self.setProperty("hover", "true")
        self.label.style().polish(self.label)
        self.icon.style().polish(self.icon)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        self.setProperty("hover", "false")
        self.label.style().polish(self.label)
        self.icon.style().polish(self.icon)
        super().leaveEvent(event)
