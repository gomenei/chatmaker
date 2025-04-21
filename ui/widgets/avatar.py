from PyQt5.QtWidgets import QLabel, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from ..config import ConfigManager

class AvatarWidget(QLabel):
    """可动态更新的圆形头像组件"""
    def __init__(self, role: str, initial_path: str, avatar_size: int):
        """
        :param role: 角色标识，'me'表示用户自己，'other'表示对方
        :param initial_path: 初始头像路径
        """
        super().__init__()
        self.role = role
        self.initial_path = initial_path
        self.avatar_size = avatar_size
        self.setMinimumSize(avatar_size, avatar_size)  # 保持合适尺寸
        
        # 连接全局配置变更信号
        self.config = ConfigManager.instance()
        self.config.avatar_changed.connect(self._on_avatar_changed)
        
        self.init_ui()
        self.load_avatar(initial_path)

    def init_ui(self):
        """初始化视觉效果"""
        self.load_style()
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/avatar.qss"))

    def load_avatar(self, path: str):
        """加载并显示头像"""
        pixmap = QPixmap(path).scaled(
            self.avatar_size, self.avatar_size, 
            Qt.KeepAspectRatioByExpanding, 
            Qt.SmoothTransformation
        )
        self.setPixmap(pixmap)

    def _on_avatar_changed(self, role: str, new_path: str):
        """响应头像变更信号"""
        if role == self.role:
            self.load_avatar(new_path)

class DoubleClickAvatarWidget(AvatarWidget):
    """双击修改的头像控件"""
    clicked = pyqtSignal()
    def __init__(self, role: str, initial_path: str, avatar_size: int):
        super().__init__(role, initial_path, avatar_size)
        # 初始化样式
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(f"双击修改{ '自己' if role=='me' else '对方' }头像")

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
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # 点击时发射信号
        super().mousePressEvent(event)
