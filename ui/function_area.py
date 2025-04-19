from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from ui.config import ConfigManager
from ui.message_widget import AvatarWidget

class FunctionPanel(QWidget):
    insert_clicked = pyqtSignal(str, bool)  # text, is_me

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # ==== 身份选择：头像 + 单选按钮 ====
        role_label = QLabel("Function")
        role_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        role_label.setAlignment(Qt.AlignCenter)  # 标题居中

        # ==== 头像行 ====
        self.me_avatar = NewAvatarWidget("me", self.config.get_avatar_path("me"), 64)
        self.other_avatar = NewAvatarWidget('other', self.config.get_avatar_path("other"), 64)
        
        # 设置头像之间的间距样式
        self.me_avatar.setContentsMargins(10, 0, 10, 0)
        self.other_avatar.setContentsMargins(10, 0, 10, 0)

        # 头像横向布局
        avatar_layout = QHBoxLayout()
        avatar_layout.addStretch()
        avatar_layout.addWidget(self.me_avatar)
        avatar_layout.addSpacing(30)
        avatar_layout.addWidget(self.other_avatar)
        avatar_layout.addStretch()

        # ==== 选择栏行 ====
        self.radio_me = QRadioButton("自己")
        self.radio_other = QRadioButton("对方")
        self.radio_me.setChecked(True)
        
        # 增大单选框字号
        radio_font = QFont("Microsoft YaHei", 10)
        self.radio_me.setFont(radio_font)
        self.radio_other.setFont(radio_font)
        
        # 单选框布局
        radio_layout = QHBoxLayout()
        radio_layout.addStretch()
        radio_layout.addWidget(self.radio_me)
        radio_layout.addSpacing(40)  # 增大选择项间距
        radio_layout.addWidget(self.radio_other)
        radio_layout.addStretch()


        # ==== 插入对话按钮 ====
        self.insert_btn = QPushButton("➕ 插入一条对话 😊")
        self.insert_btn.setFixedHeight(100)
        self.insert_btn.setFont(QFont("Microsoft YaHei", 11))
        self.insert_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px dashed #cccccc;
                border-radius: 12px;
                text-align: left;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e0ffe0;
                border-color: #07c160;
            }
        """)

        # 预留空间
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 添加布局项
        layout.addWidget(role_label)
        layout.addSpacing(10)  # 增加标题与头像间距
        layout.addLayout(avatar_layout)
        layout.addSpacing(5)  # 头像与单选框间距
        layout.addLayout(radio_layout)
        layout.addWidget(self.insert_btn)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def setup_connections(self):
        # 连接插入
        self.insert_btn.clicked.connect(self.insert_sample_message)

    def insert_sample_message(self):
        text = "双击编辑对话 😊"
        is_me = self.radio_me.isChecked()
        self.insert_clicked.emit(text, is_me)

class NewAvatarWidget(AvatarWidget):
    """可修改的头像控件"""

    def __init__(self, role: str, initial_path: str, avatar_size: int):
        """
        param
          role: 身份标识 ('me' 或 'other')
        """
        super().__init__(role, initial_path, avatar_size)

        # 初始化样式
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(f"双击修改{ '自己' if role=='me' else '对方' }头像")
        
        # 加载初始头像
        self.load_avatar(initial_path)
        
        # 连接配置更新信号
        self.config.avatar_changed.connect(self.on_global_avatar_changed)

    def mouseDoubleClickEvent(self, event):
        """双击事件处理"""
        if event.button() == Qt.LeftButton:
            # 弹出文件选择对话框
            new_path, _ = QFileDialog.getOpenFileName(
                self, 
                "选择头像文件",
                "", 
                "图片文件 (*.png *.jpg *.jpeg)"
            )
            
            if new_path:  # 用户选择了有效路径
                self.load_avatar(new_path)  # 本地立即生效
                self.config.set_avatar_path(self.role, new_path)  # 更新全局配置
                
        super().mouseDoubleClickEvent(event)

    def on_global_avatar_changed(self, role: str, path: str):
        """响应全局头像修改"""
        if role == self.role:
            self.load_avatar(path)