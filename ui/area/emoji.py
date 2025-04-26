from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QFrame, QGridLayout, QScrollArea, QSizePolicy, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon

class EmojiArea(QFrame):
    emoji_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
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

        # 测试emoji表情
        self.emojis = [
            "😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊",
            "😋", "😎", "😍", "😘", "😗", "😙", "😚", "🙂", "🤗", "🤔",
            "😐", "😑", "😶", "🙄", "😏", "😣", "😥", "😮", "🤐", "😯"
        ]
        
        self.add_emojis()

    def add_emojis(self):
        for i, emoji in enumerate(self.emojis):
            btn = QPushButton(emoji)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    background: transparent;
                    border: none;
                    padding: 5px;
                }
                QPushButton:hover {
                    background: #e0e0e0;
                    border-radius: 5px;
                }
            """)
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda _, e=emoji: self.emoji_selected.emit(e))
            self.layout.addWidget(btn, i//5, i%5)
