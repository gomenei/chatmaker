from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QFrame, QGridLayout, QScrollArea, QSizePolicy, QApplication,)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QPixmap
from ui.config import ConfigManager

class EmojiArea(QFrame):
    emoji_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.emoji_map = self.config.emoji_map
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            EmojiPanel {
                background: #f5f5f5;
                border-top: 1px solid #ddd;
            }
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        self.layout = QGridLayout(container)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, 10, 10, 10)

        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # # 测试emoji表情
        # self.emojis = [
        #     "😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊",
        #     "😋", "😎", "😍", "😘", "😗", "😙", "😚", "🙂", "🤗", "🤔",
        #     "😐", "😑", "😶", "🙄", "😏", "😣", "😥", "😮", "🤐", "😯"
        # ]
        
        self.add_emojis()

    def add_emojis(self):
        row, col = 0, 0
        for emoji_code, img_path in self.emoji_map.items():
            btn = QPushButton()
            btn.setFixedSize(40, 40)
            btn.setToolTip(emoji_code)  # 悬停显示表情代号

            btn.setStyleSheet("""
                QPushButton {
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #d3d3d3;
                    border-radius: 5px;
                }
                QPushButton:pressed {
                    background-color: #d3d3d3;
                    border-radius: 5px;
                }
            """)
            
            # 加载图片并缩放
            pixmap = QPixmap(img_path)
            if pixmap.isNull():
                print(f"警告：表情图片未找到 {img_path}")
                continue
                
            icon = QIcon(pixmap.scaled(
                30, 30, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            ))
            btn.setIcon(icon)
            btn.setIconSize(QSize(30, 30))
            
            # 点击时发送表情代号
            btn.clicked.connect(
                lambda _, code=emoji_code: self.emoji_selected.emit(code)
            )
            
            self.layout.addWidget(btn, row, col)
            col += 1
            if col >= 5:  # 每行 5 个表情
                col = 0
                row += 1

