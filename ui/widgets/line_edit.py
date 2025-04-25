from PyQt5.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QSizePolicy, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QTextDocument, QFontMetrics

class LineEditWidget(QLineEdit):
    """支持双击编辑的标题标签"""

    """如果想修改背景变得透明，用QWidget再包一层"""
    editing_finished = pyqtSignal(str)  # 编辑完成信号
    
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setReadOnly(True)
        self._preedit_text = ""  # 预编辑文本
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.transparent)
        palette.setColor(self.palette().Base, Qt.transparent)  # 重点是这个
        self.setPalette(palette)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)

        # 关键设置（核心代码）
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 水平自动扩展
        # self.setMinimumWidth(self.fontMetrics().boundingRect(self.text()).width() + 10)
        self.textChanged.connect(self.adjust_width)

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

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self.adjust_width)

    def adjust_width(self, preedit_text=""):
        """智能宽度计算（包含预编辑文本）"""
        fm = self.fontMetrics()
        base_width = fm.horizontalAdvance(self.text()) + fm.horizontalAdvance(self._preedit_text)
        # 设置最终宽度（文本宽度 + 20px边距）
        self.setFixedWidth(base_width + 20)
    
    def inputMethodEvent(self, event):
        super().inputMethodEvent(event)
        self._preedit_text = event.preeditString()

        self.adjust_width()

class EditableLabel(QWidget):
    editing_finished = pyqtSignal(str)

    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._text = text
        self.label = QLabel(text)
        self.edit = QLineEdit(text)
        self.edit.hide()

        self.label.setObjectName("TitleLabel")
        self.edit.setObjectName("TitleLabel")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)

        self.label.mouseDoubleClickEvent = self.start_edit
        self.edit.editingFinished.connect(self.finish_edit)

    def start_edit(self, event):
        self.label.hide()
        self.edit.setText(self.label.text())
        self.edit.show()
        self.edit.setFocus()

    def finish_edit(self):
        new_text = self.edit.text()
        self._text = new_text
        self.label.setText(new_text)
        self.label.show()
        self.edit.hide()
        self.editing_finished.emit(new_text)

    def setText(self, text):
        self._text = text
        self.label.setText(text)
        self.edit.setText(text)

    def text(self):
        return self._text