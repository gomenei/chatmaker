from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QApplication, QFileDialog, QSizePolicy
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
        self.set_adaptive_size()  # 根据屏幕尺寸调整窗口大小
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

        self.chat_area = ChatArea(self)
        main_layout.addWidget(self.chat_area, stretch=2)

        self.function_panel = FunctionArea()
        main_layout.addWidget(self.function_panel, stretch=1)
        
        # 连接插入功能
        self.function_panel.insert_clicked.connect(self.handle_insert_message)
        self.function_panel.export_clicked.connect(self.export_chat_as_image)

        self.setCentralWidget(main_widget)

    def set_adaptive_size(self):
        """根据当前屏幕尺寸调整窗口大小"""
        screen = QApplication.primaryScreen()  # 获取主屏幕
        screen_rect = screen.availableGeometry()  # 获取可用屏幕区域（排除任务栏等）
        # 设置窗口大小为屏幕宽度的30%和高度的70%（可根据需要调整比例）
        width = int(screen_rect.width() * (81 / 256))  
        height = int(screen_rect.height() * (150 / 191))  
        print("main_window size =", (width, height))
        self.resize(width, height)  # 调整窗口大小
        self.setFixedWidth(width)
        # 让窗口居中显示
        self.move(
            screen_rect.left() + (screen_rect.width() - width) // 2,
            screen_rect.top() + (screen_rect.height() - height) // 2
        )

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
            case "图片消息":
                file_path, _ = QFileDialog.getOpenFileName(
                    self, "选择图片", "", 
                    "图片文件 (*.png *.jpg *.jpeg);;所有文件 (*)"
                )
                if file_path:
                    self.chat_area.scroll_area.add_message(file_path, is_me, avatar, message_type="photo")
            case "表情包":
                file_path, _ = QFileDialog.getOpenFileName(
                    self, "选择GIF表情包", "", 
                    "GIF动画 (*.gif);;所有文件 (*)"
                )
                if file_path:
                    self.chat_area.scroll_area.add_message(file_path, is_me, avatar, message_type="gif")
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