from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QSpacerItem
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from ui.area.scroll import ScrollArea
from ui.area.input import InputArea
from ui.config import ConfigManager
from ui.widgets.status import StatusWidget
from ui.widgets.title import TitleWidget

class ChatArea(QWidget):
    '''
    聊天组件:
        顶部状态栏
        标题栏
        消息展示区
        消息发送区
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.message_widgets = [] # 消息队列
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        # 主布局设置
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        # ===== 1. 手机状态栏 (全Emoji版本) =====
        self.status_bar = StatusWidget()
        # ===== 2. 微信风格标题栏 =====
        self.title_bar = TitleWidget("请输入昵称")
        # self.title_bar.back_clicked.connect(self.handle_back)
        # ===== 3. 原有聊天区域 =====
        self.scroll_area = ScrollArea()
        self.input_widget = InputArea()
        
        # ===== 组合所有组件 =====
        self.main_layout.addWidget(self.status_bar)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.input_widget)
        
        # 设置布局伸缩权重
        self.main_layout.setStretch(0, 0)  # 状态栏
        self.main_layout.setStretch(1, 0)  # 标题栏
        self.main_layout.setStretch(2, 1)  # 消息区
        self.main_layout.setStretch(3, 0)  # 输入区

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
