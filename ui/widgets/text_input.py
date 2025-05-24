# ui/widgets/text_input.py
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QFontMetrics
from ui.config import ConfigManager

class TextInput(QTextEdit):
    """通用文本输入框组件（支持动态高度调整和Enter发送）"""
    send_trigger = pyqtSignal()
    height_changed = pyqtSignal(int)
    text_input = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.emoji_map = self.config.emoji_map
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        parent_width = self.parent().width()
        self.origin_width = int(parent_width * 21 / 30)
        self.input_width = int(parent_width * 0.63)
        self.orgin_height = int(parent_width * 0.138)
        self.setFixedHeight(int(self.orgin_height))
        self.setFont(QFont("黑体", 12))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # 动态高度计算
        font_metrics = self.fontMetrics()
        line_height = font_metrics.lineSpacing()
        # print("parent width = ", self.parent().width())
        print("line_height = ", line_height)
        # print("height =", self.height())
        self.min_input_height = self.orgin_height  # 1行 + padding
        self.max_input_height = 3 * line_height + self.orgin_height  # 最大8行
        # self.setMinimumHeight(self.min_input_height)
        self.setMaximumHeight(self.max_input_height)

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
            self.setFixedWidth(self.input_width)
            self.text_input.emit(True)
        else:
            self.setFixedWidth(self.origin_width)
            self.text_input.emit(False)

        """动态调整输入框高度"""
        doc = self.document()
        margin = self.contentsMargins()
        print("margin height =", margin.top() + margin.bottom())
        desired_height = doc.documentLayout().documentSize().height() + margin.top() + margin.bottom()
        # desired_height = min(max(desired_height, self.min_input_height), self.max_input_height)
        html_text = doc.toHtml()
        print("text height =", desired_height)
        self.setFixedHeight(int(self.orgin_height))
        # self.setFixedHeight(int(desired_height))
    
    def get_emoji_html(self, emoji_code):
        """返回表情图片的HTML格式"""
        if emoji_code in self.emoji_map:
            return f'<img src="{self.emoji_map[emoji_code]}" width="24" height="24">'
        return ""

    def insert_emoji(self, emoji_code):
        """用HTML插入表情图片（替代QTextImageFormat方式）"""
        cursor = self.textCursor()
        html = self.get_emoji_html(emoji_code)
        if html:  # 只插入有效的表情
            cursor.insertHtml(html)