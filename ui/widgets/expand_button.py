from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, 
                            QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtGui import QFont, QPainter

class ExpandButton(QWidget):
    def __init__(self):
        super().__init__()
        # 允许父控件透明（避免裁剪超出部分）
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 主布局（水平排列：扩展区域 + 按钮）
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # 扩展区域（左侧，初始宽度0）
        self.expand_widget = QWidget()
        self.expand_widget.setFixedWidth(0)
        self.expand_widget.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #07c160;
            border-radius: 12px 0 0 12px;  /* 左侧圆角 */
            border-right: none;
            padding: 10px;
        """)
        # 扩展区域内部内容
        expand_layout = QVBoxLayout(self.expand_widget)
        expand_layout.addWidget(QLabel("💬 从左侧弹出"))
        # 按钮（右侧）
        self.button = QPushButton("➕ 插入一条对话 😊")
        self.button.setFixedHeight(100)
        self.button.setFont(QFont("Microsoft YaHei", 11))
        self.button.setStyleSheet("""
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
        # 将扩展区域和按钮添加到布局（注意顺序）
        self.layout.addWidget(self.expand_widget)
        self.layout.addWidget(self.button)
        # 动画控制扩展区域宽度
        self.animation = QPropertyAnimation(self.expand_widget, b"minimumWidth")
        self.animation.setDuration(200)
        # 绑定鼠标事件
        self.button.installEventFilter(self)
    def eventFilter(self, obj, event):
        if obj == self.button:
            if event.type() == event.Enter:
                self._expand()
            elif event.type() == event.Leave:
                self._collapse()
        return super().eventFilter(obj, event)
    def _expand(self):
        """向左展开（宽度从0 -> 200）"""
        self.animation.setStartValue(0)
        self.animation.setEndValue(200)
        self.animation.start()
    def _collapse(self):
        """收缩回左侧"""
        self.animation.setStartValue(self.expand_widget.width())
        self.animation.setEndValue(0)
        self.animation.start()
    def paintEvent(self, event):
        """解决WA_TranslucentBackground下背景透明问题"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
