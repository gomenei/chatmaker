from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from ui.area.chat import ChatArea
from ui.area.function import FunctionArea
from ui.config import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.config = ConfigManager.instance()

    def init_ui(self):
        self.setWindowTitle("ChatMaker")
        self.resize(750, 1000)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        self.chat_area = ChatArea()
        main_layout.addWidget(self.chat_area, stretch=2)

        self.function_panel = FunctionArea()
        main_layout.addWidget(self.function_panel, stretch=1)

        # 连接插入功能
        self.function_panel.insert_clicked.connect(self.handle_insert_message)

        self.setCentralWidget(main_widget)

    def handle_insert_message(self, text, is_me):
        """处理功能栏插入的消息"""
        avatar = self.config.get_avatar_path("me") if is_me else self.config.get_avatar_path("other")
        self.chat_area.scroll_area.add_message(text, is_me, avatar)