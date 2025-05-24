import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, 
    QPushButton, QFileDialog, QLabel
)
from PyQt5.QtGui import QTextCursor, QTextImageFormat, QMovie
from PyQt5.QtCore import Qt, QSize

class ImageAndGifWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()