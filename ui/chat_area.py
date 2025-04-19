from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QFontMetrics, QTextOption
from ui.message_widget import MessageWidget
from ui.config import ConfigManager

class ChatArea(QWidget):
    '''
    聊天组件
    垂直分为两部分，上方是消息展示区，下方是聊天发送区
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.message_widgets = [] # 消息队列
        self.init_ui()
        self.setup_connections()
        self.test_message()

    def init_ui(self):
        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # 消息展示区
        self.scroll_area = ScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # 输入区域
        self.input_widget = InputArea()

        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.input_widget)

    def setup_connections(self):
        # 连接发送信号与消息处理
        self.input_widget.send_clicked.connect(self.handle_send_message)

    def add_message(self, text, is_me, avatar_path):
        # 创建消息气泡
        message_widget = MessageWidget(
            text=text,
            is_me=is_me,  # 标记为自己发送的消息
            avatar_path=avatar_path  # 指定头像路径
        )

        # 将消息添加到容器
        self.scroll_area.message_layout.addWidget(message_widget)
        self.message_widgets.append(message_widget)
        message_widget.text_deleted.connect(self.remove_message)

    def remove_message(self, widget):
        if widget in self.message_widgets:
            self.scroll_area.message_layout.removeWidget(widget)
            self.message_widgets.remove(widget)
            widget.deleteLater()
            # QTimer.signleShot(0, self._updata_layout_spacing)

    def handle_send_message(self):
        """处理消息发送"""
        text = self.input_widget.input_box.toPlainText().strip()
        if not text:
            return
        
        self.add_message(text, True, self.config.get_avatar_path("me"))
        # self.add_message("自动回复", False, "./fig/default.jpeg")

        # 清空输入框
        self.input_widget.input_box.clear()

        # 自动滚动到底部
        QTimer.singleShot(50, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        """滚动到底部"""
        scroll_bar = self.scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def test_message(self):
        self.add_message("这是一个非常长的文本，用于测试是否会根据容器宽度自动换行显示多行内容。", True, self.config.get_avatar_path("me"))
        self.add_message("ThisIsAVeryLongEnglishWordWithoutSpacesToTestWrappingBehavior", False, self.config.get_avatar_path("other"))

class ScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWidgetResizable(True) 
        self.setFrameShape(QFrame.NoFrame)
        
        # 消息容器
        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setAlignment(Qt.AlignTop)
        self.message_layout.setSpacing(4)
        self.setWidget(self.message_container)

        # 样式设置
        self.message_container.setStyleSheet("background: white;")
        self.setStyleSheet("""
            QScrollArea { border: none; }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 4px;
            }
        """)

class InputArea(QWidget):
    send_clicked = pyqtSignal()  # 新增发送信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 文本输入框
        self.input_box = TextInput(self)

        # 发送按钮
        self.send_btn = QPushButton("发送")
        self.send_btn.setFixedSize(70, 50)
        self.send_btn.setFont(QFont("Microsoft YaHei", 10))

        self.main_layout.addWidget(self.input_box, alignment=Qt.AlignBottom)
        self.main_layout.addWidget(self.send_btn, alignment=Qt.AlignBottom)

        # 设置样式
        self.setStyleSheet("""
            /* 输入框主体样式 */
            QTextEdit {
                background: #ffffff;      /* 微信同款浅灰背景 */
                border-radius: 8px;      /* 更大的圆角 */
                padding: 8px 12px;       /* 舒适的边距 */
                color: #333;              /* 文本颜色 */
            }
            /* 输入框占位符文字颜色 */
            QTextEdit::placeholder {
                color: #999;
                font-style: normal;       /* 取消斜体 */
            }
            /* 发送按钮样式增强 */
            QPushButton {
                background: #07c160;      /* 与聚焦色统一的微信绿色 */
                color: white;
                border: none;
                border-radius: 6px;       /* 匹配输入框圆角 */
                font-weight: 500;
                margin-left: 8px;         /* 输入框与按钮间距 */
            }
            QPushButton:hover { background: #05a050; }
            QPushButton:pressed { background: #048a45; }
        """)

    def setup_connections(self):
        # 连接按钮点击事件
        self.send_btn.clicked.connect(self.on_send_clicked)
        # Enter键快速发送
        self.input_box.send_trigger.connect(self.on_send_clicked)

    def on_send_clicked(self):
        """触发发送信号"""
        self.send_clicked.emit()

class TextInput(QTextEdit):
    send_trigger = pyqtSignal()  # Enter发送信号
    height_changed = pyqtSignal(int)  # 高度变化信号（可选）

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        self.setFont(QFont("黑体", 12))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QTextEdit.WidgetWidth)           # 按控件宽度换行
        font_metrics = self.fontMetrics()
        line_height = font_metrics.lineSpacing()
        
        self.min_input_height = line_height + 8 * 3  # 最小一行高度（含边距）
        self.max_input_height = 4 * line_height + 8 * 3  # 最大八行高度
        self.setMinimumHeight(self.min_input_height)
        self.setMaximumHeight(self.max_input_height)
        self.adjust_height()

    def setup_connections(self):
        # 监听文本变化自动调整高度
        self.textChanged.connect(self.adjust_height)

    def keyPressEvent(self, event):
        """Enter发送消息，Shift+Enter换行"""
        if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
            # 纯Enter：触发发送
            self.send_trigger.emit()
            event.accept()
        else:
            super().keyPressEvent(event)

    def adjust_height(self):
        """动态调整输入框高度"""
        doc = self.document()
        margin = self.contentsMargins()
        desired_height = doc.documentLayout().documentSize().height() + margin.top() + margin.bottom()
        desired_height = min(max(desired_height, self.min_input_height), self.max_input_height)
        self.setFixedHeight(int(desired_height))


