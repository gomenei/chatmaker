# ui/widgets/text_input.py
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QFontMetrics

class TextInput(QTextEdit):
    """通用文本输入框组件（支持动态高度调整和Enter发送）"""
    send_trigger = pyqtSignal()
    height_changed = pyqtSignal(int)
    text_input = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        self.setFont(QFont("黑体", 12))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # 动态高度计算
        font_metrics = self.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.min_input_height = line_height + 43  # 1行 + padding
        self.max_input_height = 4 * line_height + 43  # 最大8行
        self.setMinimumHeight(self.min_input_height)
        self.setMaximumHeight(self.max_input_height)

        #设置初始宽度
        self.setFixedWidth(350)

        self.adjust_size()

    def setup_connections(self):
        self.textChanged.connect(self.adjust_size)

    def keyPressEvent(self, event):
        """Enter发送消息，Shift+Enter换行"""
        if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
            self.send_trigger.emit()
            event.accept()
        else:
            super().keyPressEvent(event)

    def adjust_size(self):
        """动态调整输入框形状"""
        """动态调整输入框宽度"""
        if self.toPlainText().strip():
            self.setFixedWidth(308)
            self.text_input.emit(True)
        else:
            self.setFixedWidth(350)
            self.text_input.emit(False)

        """动态调整输入框高度"""
        doc = self.document()
        margin = self.contentsMargins()
        desired_height = doc.documentLayout().documentSize().height() + margin.top() + margin.bottom()
        desired_height = min(max(desired_height, self.min_input_height), self.max_input_height)
        self.setFixedHeight(int(desired_height))