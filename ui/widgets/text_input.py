# ui/widgets/text_input.py
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal, QMargins
from PyQt5.QtGui import QFont, QFontMetrics, QTextBlockFormat
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
        self.origin_width = int(parent_width * (23 / 36))
        self.input_width = int(parent_width * (329 / 540))
        self.origin_height = int(parent_width * (53 / 540))

        # 初始化字体并调整到合适大小
        self._base_font = QFont("黑体", 14)
        self.adjust_font_to_fit_height(self.origin_height * (1 / 2))

         # 清除所有边距和文档边距
        margin = int(self.origin_height * (1 / 4))
        # self.setContentsMargins(QMargins(margin, margin, margin, margin))
        self.document().setDocumentMargin(margin) 
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setFixedSize(self.origin_width, self.origin_height)

        font_metrics = QFontMetrics(self.font())
        line_height = font_metrics.lineSpacing()
        self.min_input_height = self.origin_height  # 1行高度（已匹配）
        self.max_input_height = 3 * line_height + self.origin_height  # 最大4行

    def adjust_font_to_fit_height(self, target_height):
        """调整字体大小使行高精确匹配目标高度"""
        test_font = self._base_font
        font_metrics = QFontMetrics(test_font)
        
        # 计算需要调整的缩放因子
        current_height = font_metrics.lineSpacing()
        if current_height == 0:
            return
            
        scale_factor = target_height / current_height
        test_font.setPointSizeF(test_font.pointSizeF() * scale_factor)
        
        # 验证调整后的高度
        adjusted_metrics = QFontMetrics(test_font)
        adjusted_height = adjusted_metrics.lineSpacing()

        # 测试emoji的大小，使其刚好符合插入的比例
        # cursor = self.textCursor()
        # doc = self.document()
        # initial_height = doc.size().height()
        # print(initial_height)
        # self.delta_height = 0
        # cursor.insertHtml(self.get_emoji_html(0))
        # self.delta_height = doc.size().height() - initial_height
        # print(self.delta_height)
        # cursor.deletePreviousChar()
        
        if abs(adjusted_height - target_height) <= 1:  # 允许1像素误差
            self.setFont(test_font)
        else:
            print(f"无法精确匹配行高 {target_height}px, 使用最近似值 {adjusted_height}px")
            self.setFont(test_font)

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
        font_metrics = QFontMetrics(self.font())
        doc_height = doc.documentLayout().documentSize().height()
        margin_height = self.contentsMargins().top() + self.contentsMargins().bottom()
        
        doc = self.document()
        print("--- 文档状态 ---")
        print(f"行高: {QFontMetrics(self.font()).lineSpacing()}px")
        print(f"文档总高度: {doc.size().height()}px")
        print(f"内容边距: {doc.documentMargin()}px")
        
        # 打印段落格式
        cursor = self.textCursor()
        block_format = cursor.blockFormat()
        print(f"段落行高类型: {block_format.lineHeightType()}")
        print(f"段落行高值: {block_format.lineHeight()}")
        if doc_height >= self.max_input_height:
            self.setFixedHeight(int(self.max_input_height))
        else:
            self.setFixedHeight(int(doc_height))
        # self.setFixedHeight(int(desired_height))
    
    def get_emoji_html(self, emoji_code):
        font_metrics = QFontMetrics(self.font())
        emoji_size = font_metrics.lineSpacing()
        print("emoji width", emoji_size)
        """返回表情图片的HTML格式"""
        if emoji_code in self.emoji_map:
            return f'''<img src="{self.emoji_map[emoji_code]}" 
                        width="{emoji_size}" 
                        height="{emoji_size}"
                        style="display: block;
                vertical-align: top;  /* 关键：强制顶部对齐 */
                margin: 0;
                padding: 0;
                line-height: {emoji_size}px"
         '''
        return ""

    def insert_emoji(self, emoji_code):
        """用HTML插入表情图片（替代QTextImageFormat方式）"""
        cursor = self.textCursor()
        html = self.get_emoji_html(emoji_code)
        if html:  # 只插入有效的表情
            cursor.insertHtml(html)
            