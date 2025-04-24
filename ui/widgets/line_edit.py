from PyQt5.QtWidgets import QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class LineEditWidget(QLineEdit):
    """支持双击编辑的标题标签"""
    editing_finished = pyqtSignal(str)  # 编辑完成信号
    
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setReadOnly(True)
        
    def mouseDoubleClickEvent(self, event):
        """双击事件处理"""
        self.setReadOnly(False)
        super().mouseDoubleClickEvent(event)
    
    def focusOutEvent(self, event):
        self.setReadOnly(True)
        return super().focusOutEvent(event)
    
    def keyPressEvent(self, event):
        """按回车键保存"""
        if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
            self.editing_finished.emit(self.text())
            self.clearFocus()
        else:
            super().keyPressEvent(event)