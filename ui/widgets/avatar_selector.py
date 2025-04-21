from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui.config import ConfigManager
from ui.widgets.avatar import DoubleClickAvatarWidget

class AvatarSelectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config = ConfigManager().instance()
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        # ==== 主布局 ====
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # ==== 头像行 ====
        self.me_avatar = DoubleClickAvatarWidget("me", self.config.get_avatar_path("me"), 64)
        self.other_avatar = DoubleClickAvatarWidget('other', self.config.get_avatar_path("other"), 64)

        # ==== 单选按钮行 ====
        self.radio_me = QRadioButton("自己")
        self.radio_other = QRadioButton("对方")
        self.radio_me.setChecked(True)
        
        # 设置字体
        radio_font = QFont("Microsoft YaHei", 10)
        self.radio_me.setFont(radio_font)
        self.radio_other.setFont(radio_font)
        
        # 头像布局
        avatar_layout = QHBoxLayout()
        avatar_layout.addStretch()
        avatar_layout.addWidget(self.me_avatar)
        avatar_layout.addSpacing(30)
        avatar_layout.addWidget(self.other_avatar)
        avatar_layout.addStretch()
        main_layout.addLayout(avatar_layout)
        
        # 单选按钮布局
        radio_layout = QHBoxLayout()
        radio_layout.addStretch()
        radio_layout.addWidget(self.radio_me)
        radio_layout.addSpacing(40)
        radio_layout.addWidget(self.radio_other)
        radio_layout.addStretch()
        main_layout.addLayout(radio_layout)
    
    def setup_connections(self):
        # 点击头像时切换单选按钮
        self.me_avatar.clicked.connect(lambda: self.set_role(True))
        self.other_avatar.clicked.connect(lambda: self.set_role(False))

    def set_role(self, is_me):
        """设置当前角色（以编程方式切换）"""
        self.radio_me.setChecked(is_me)
        self.radio_other.setChecked(not is_me)