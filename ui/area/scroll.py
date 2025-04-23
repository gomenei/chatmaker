from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from ui.config import ConfigManager
from ui.widgets.message import MessageWidget

class ScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.message_widgets = [] # 消息队列
        self.init_ui()
        self.load_style()
        self.test_message()

    def init_ui(self):
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        
        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setAlignment(Qt.AlignTop)
        self.message_layout.setSpacing(4)
        self.setWidget(self.message_container)

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/scroll.qss"))

    def scroll_to_bottom(self):
        """滚动到底部"""
        scroll_bar = self.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        QTimer.singleShot(50, self.scroll_to_bottom)
    
    def add_message(self, text, is_me, avatar_path):
        message_widget = MessageWidget(
            text=text,
            is_me=is_me,  
            role="me" if is_me else "other",
            avatar_path=avatar_path 
        )

        # 将消息添加到容器
        self.message_layout.addWidget(message_widget)
        self.message_widgets.append(message_widget)
        message_widget.text_deleted.connect(self.remove_message)
        message_widget.text_up.connect(self.move_message_up)
        message_widget.text_down.connect(self.move_message_down)
        self.scroll_to_bottom()  # 滚动到底部

    def remove_message(self, widget):
        if widget in self.message_widgets:
            self.message_layout.removeWidget(widget)
            self.message_widgets.remove(widget)
            widget.deleteLater()
    
    def move_message_up(self, widget):
        """将消息向上移动"""
        index = self.message_layout.indexOf(widget)
        if index > 0:  # 如果不是第一个
            self.message_layout.removeWidget(widget)
            self.message_layout.insertWidget(index - 1, widget)
    
    def move_message_down(self, widget):
        """将消息向下移动"""
        index = self.message_layout.indexOf(widget)
        if index < self.message_layout.count() - 1:  # 如果不是最后一个
            self.message_layout.removeWidget(widget)
            self.message_layout.insertWidget(index + 1, widget)

    def test_message(self):
        self.add_message("这是一个非常长的文本，用于测试是否会根据容器宽度自动换行显示多行内容。", True, self.config.get_avatar_path("me"))
        self.add_message("ThisIsAVeryLongEnglishWordWithoutSpacesToTestWrappingBehavior", False, self.config.get_avatar_path("other"))
