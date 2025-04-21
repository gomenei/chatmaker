from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
                            QPushButton, QLabel)
from PyQt5.QtCore import Qt, pyqtSignal
from ..config import ConfigManager
from ui.widgets.avatar import AvatarWidget
from ui.widgets.bubble import BubbleWidget

class MessageWidget(QWidget):
    """带头像的消息气泡组件，支持双向显示和内容编辑"""
    text_edited = pyqtSignal(str)  # 内容修改信号
    text_deleted = pyqtSignal(QWidget)
    text_up = pyqtSignal(QWidget)
    text_down = pyqtSignal(QWidget)

    def __init__(self, text: str, is_me: bool, role: str, avatar_path: str):
        super().__init__()
        self.is_me = is_me        # 消息方向标识
        self.role = role          # 群成员标识
        self.avatar_path = avatar_path
        self.text = text 
        self.init_ui()
        self.load_style()
        
    def init_ui(self):
        """初始化界面布局"""
        self.setup_avatar()
        self.setup_bubble(self.text)
        self.setup_button()

        """主布局设置"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # 优化边距

        """气泡 + 头像设置"""
        self.chatbubble_layout = QHBoxLayout()
        
        if self.is_me:
            self.chatbubble_layout.addStretch()
            self.chatbubble_layout.addWidget(self.bubble)
            self.chatbubble_layout.addWidget(self.avatar_label, alignment=Qt.AlignTop)
        else:
            self.chatbubble_layout.addWidget(self.avatar_label, alignment=Qt.AlignTop)
            self.chatbubble_layout.addWidget(self.bubble)
            self.chatbubble_layout.addStretch()

        self.main_layout.addLayout(self.chatbubble_layout)
        self.main_layout.addWidget(self.btn_group, alignment=Qt.AlignHCenter)
        self.setLayout(self.main_layout)

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/message.qss"))

    def setup_avatar(self):
        self.avatar_label = AvatarWidget(
            role="me" if self.is_me else "other", 
            initial_path=self.avatar_path,
            avatar_size=40
        )

    def setup_button(self):
        """ 创建悬浮控制按钮 """
        self.btn_group = QFrame()
        self.btn_group.setObjectName("btn_group")
        self.btn_group.hide()

        # 按钮布局
        layout = QHBoxLayout(self.btn_group)
        layout.setContentsMargins(5, 0, 5, 0)
        # 操作按钮
        self.btn_up = self.setup_signal_button("↑", "上移", "btn_up", layout)
        self.btn_down = self.setup_signal_button("↓", "下移", "btn_down", layout)
        self.btn_delete = self.setup_signal_button("×", "删除", "btn_delete", layout)
        
        self.btn_delete.clicked.connect(lambda: self.text_deleted.emit(self))
        self.btn_down.clicked.connect(lambda: self.text_down.emit(self))
        self.btn_up.clicked.connect(lambda: self.text_up.emit(self))

    def setup_signal_button(self, icon, text, btn_name, parent_layout):
        """ 创建图标+文字的组合按钮 """
        btn_container = QWidget()  # 容器用于打包图标和文字
        btn_container.setObjectName("btn_container")
        # 整体横向布局
        layout = QHBoxLayout(btn_container)
        layout.setContentsMargins(15, 0, 5, 0)
        layout.setSpacing(2)

        # -- 圆形图标部分 --
        icon_btn = QPushButton(icon)
        icon_btn.setObjectName(btn_name)
        icon_btn.setFixedSize(28, 28)  # 圆形直径
        layout.addWidget(icon_btn)
        
        # -- 文字描述部分 --
        text_label = QLabel(text)
        text_label.setObjectName("btn_text")
        layout.addWidget(text_label)
        
        # 传递点击事件（容器整体可点击）
        btn_container.mousePressEvent = lambda e: icon_btn.click()  
        parent_layout.addWidget(btn_container)
        
        return icon_btn  # 返回实际按钮用于信号连接

    def setup_bubble(self, text: str):
        """使用 QTextEdit 实现消息气泡"""      
        self.bubble = BubbleWidget(text) 
        self.bubble.setObjectName("bubble_me" if self.is_me else "bubble_other")

    def enterEvent(self, event):
        """ 鼠标进入显示控制按钮 """
        # self.btn_group.move(self.width()-110, 10)
        self.btn_group.show()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """ 鼠标离开隐藏按钮 """
        self.btn_group.hide()
        super().leaveEvent(event)