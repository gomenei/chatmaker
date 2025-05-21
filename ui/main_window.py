from PyQt5.QtGui import QIcon, QPixmap, QPainter
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
        self.setFixedSize(750, 1000)
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f7f7;
            }
        """)
        # 移除标题栏
        # self.setWindowFlag(Qt.FramelessWindowHint)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.chat_area = ChatArea()
        main_layout.addWidget(self.chat_area, stretch=2)

        self.function_panel = FunctionArea()
        main_layout.addWidget(self.function_panel, stretch=1)

        # 连接插入功能
        self.function_panel.insert_clicked.connect(self.handle_insert_message)
        self.function_panel.export_clicked.connect(self.export_chat_as_image)

        self.setCentralWidget(main_widget)

    def handle_insert_message(self, text, is_me):
        """处理功能栏插入的消息"""
        avatar = self.config.get_avatar_path("me") if is_me else self.config.get_avatar_path("other")
        match text:
            case "退出":
                self.close()
            case "文字消息":
                self.chat_area.scroll_area.add_message("双击编辑文字", is_me, avatar)
            case "语音消息":
                self.chat_area.scroll_area.add_message("1", is_me, avatar, message_type="voice")
            case "语音通话":
                self.chat_area.scroll_area.add_message("2", is_me, avatar, message_type="voicecall")
            case "视频通话":
                self.chat_area.scroll_area.add_message("3", is_me, avatar, message_type="videocall")
            case _:  # 默认情况（类似 default）
                self.chat_area.scroll_area.add_message("功能暂未实现", is_me, avatar)

    def export_chat_as_image(self):
        visible_width = self.chat_area.width()
        visible_height = self.chat_area.height()
    
        scale_factor = 2
        export_width = visible_width * scale_factor
        export_height = visible_height * scale_factor
    
        image = QPixmap(export_width, export_height)
        image.fill(Qt.white)
    
        # 渲染左侧聊天区，不包括右边功能栏
        painter = QPainter(image)
        painter.scale(scale_factor, scale_factor)
        self.chat_area.render(painter)
        painter.end()

        file_path, _ = QFileDialog.getSaveFileName(self, "保存聊天截图", "微信聊天模拟器截图", "PNG 图片 (*.png)")
        if file_path:
            image.save(file_path)