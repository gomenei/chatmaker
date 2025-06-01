from PyQt5.QtWidgets import QSizePolicy, QTextBrowser, QTextEdit, QLabel
from PyQt5.QtGui import QTextDocument, QFontMetrics, QTextImageFormat, QTextCursor, QTextOption, QMovie
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSizeF
from sympy.printing.pretty.pretty_symbology import line_width
from ui.config import ConfigManager

class BubbleWidget(QTextEdit):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.config = ConfigManager().instance()
        self.emoji_map = self.config.emoji_map
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

        self.setContentsMargins(0, 0, 0, 0)
        self.document().setDocumentMargin(0)

        self.setMaximumWidth(300)
        self.max_width = 300  # 最大宽度
        # 设置初始文字
        self.setText(self.text)
        self.setReadOnly(True)

        self.document().setDocumentMargin(6)

        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        self.document().setDocumentMargin(6)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.document().setUseDesignMetrics(True)  # 添加精确度量

        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        # 统一设置文档边距（与QSS的padding匹配）
        self.document().setDocumentMargin(8)  # 对应QSS中的padding:8px
        self.setContentsMargins(12, 8, 12, 8)  # 总边距=文档边距+控件边距
        
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
        if not self.document():  # 新增文档存在性检查
            return

        doc = self.document()
        try:
            doc.setPageSize(QSizeF(max(self.max_width - 24, 10), 10000))  # 防止负值
            doc.adjustSize()

            ideal_width = min(doc.idealWidth(), self.max_width - 24)
            actual_height = doc.size().height()

            final_width = min(ideal_width + 24, self.max_width)
            final_height = actual_height + 16

            self.setFixedSize(int(final_width), int(final_height))
        except Exception as e:
            print(f"Size update error: {str(e)}")  # 添加异常捕获

    def inputMethodEvent(self, event):
        super().inputMethodEvent(event)
        preedit_text = event.preeditString()

        self.update_size(preedit_text)  # 输入法拼音输入时也调整大小

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, lambda: self.update_size())  # 延迟确保布局完成
        #QTimer.singleShot(30, lambda: self.update_size())  # 二次刷新解决图片加载延迟

    def get_emoji_html(self, emoji_code):
        font_metrics = QFontMetrics(self.font())
        emoji_size = font_metrics.lineSpacing()
        # print("emoji width", emoji_size)
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

    # def insert_emoji(self, emoji_code):
    #     """使用QTextImageFormat插入表情"""
    #     if emoji_code not in self.emoji_map:
    #         return

    #     cursor = self.textCursor()
    #     image_format = QTextImageFormat()
    #     image_format.setName(self.emoji_map[emoji_code])
    #     image_format.setWidth(20)
    #     image_format.setHeight(20)

    #     # 插入图片并确保光标位置更新
    #     cursor.insertImage(image_format)
    #     self.setTextCursor(cursor)

    #     self.document().markContentsDirty(0, self.document().characterCount())
    #     self.update_size()
