from PyQt5.QtWidgets import QSizePolicy, QTextBrowser, QTextEdit
from PyQt5.QtGui import QTextDocument, QFontMetrics
from PyQt5.QtCore import Qt, QTimer

class BubbleWidget(QTextEdit):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.initUI()
        self.setup_connections()

    def initUI(self): 
        # 设置尺寸策略（水平可扩展，垂直随内容变化）
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

         # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 按控件宽度自动换行
        self.setLineWrapMode(QTextBrowser.WidgetWidth)

        self.setMaximumWidth(300)
        self.max_width = 300  # 最大宽度
        # 设置初始文字
        self.setText(self.text)
        self.setReadOnly(True)
    
    def setup_connections(self):
        self.mouseDoubleClickEvent = self.enter_edit_mode
        self.focusOutEvent = self.exit_edit_mode
        self.keyPressEvent = self.editor_key_press_event
        self.textChanged.connect(self.update_size)
    
    def enter_edit_mode(self, event):
        self.setReadOnly(False)
    
    def exit_edit_mode(self, event):
        self.setReadOnly(True)
    
    def editor_key_press_event(self, event):
        """按回车键保存"""
        if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
            self.clearFocus()
        else:
            QTextEdit.keyPressEvent(self, event)

    def update_size(self, preedit_text=""):
        doc: QTextDocument = self.document()
        text = doc.toPlainText()
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(text) + font_metrics.width(preedit_text)
        # 限制最大宽度
        doc.setTextWidth(self.max_width - 12)

        content_width = min(text_width + 30, self.max_width)
        # 重新计算高度（基于设定的 textWidth）
        content_height = doc.size().height()

        # 更新控件尺寸
        self.setFixedWidth(int(content_width) + 12)
        self.setFixedHeight(int(content_height) + 18)

    def inputMethodEvent(self, event):
        super().inputMethodEvent(event)
        preedit_text = event.preeditString()

        self.update_size(preedit_text)  # 输入法拼音输入时也调整大小

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self.update_size)
