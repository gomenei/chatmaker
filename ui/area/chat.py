from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer
from ui.area.scroll import ScrollArea
from ui.area.input import InputArea
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

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        
        self.scroll_area = ScrollArea()
        self.input_widget = InputArea()
        
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.input_widget)

    def setup_connections(self):
        # 连接发送信号与消息处理
        self.input_widget.send_clicked.connect(self.handle_send_message)

    def handle_send_message(self):
        """处理消息发送"""
        text = self.input_widget.input_box.toPlainText().strip()
        if not text:
            return
        
        self.scroll_area.add_message(text, True, self.config.get_avatar_path("me"))
        # self.add_message("自动回复", False, "./fig/default.jpeg")
        self.input_widget.input_box.clear() # 清空输入框
        self.scroll_area.scroll_to_bottom() # 自动滚动到底部
