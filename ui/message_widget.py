from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QSizePolicy, QTextBrowser, QTextEdit, QFrame, QPushButton
from PyQt5.QtGui import QPixmap, QMouseEvent, QTextDocument, QKeyEvent, QFontMetrics, QTextOption
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QSize, QEvent
from ui.config import ConfigManager

class MessageWidget(QWidget):
    """带头像的消息气泡组件，支持双向显示和内容编辑"""
    text_edited = pyqtSignal(str)  # 内容修改信号
    text_deleted = pyqtSignal(QWidget)

    def __init__(self, text: str, is_me: bool, avatar_path: str):
        super().__init__()
        self.is_me = is_me        # 消息方向标识
        self.avatar_path = avatar_path
        self.text = text # 保留原始消息
        self.init_ui()
        self.setup_style()
        
    def init_ui(self):
        """初始化界面布局"""

        """主布局设置"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # 优化边距

        """气泡 + 头像设置"""
        self.chatbubble_layout = QHBoxLayout()
        self.avatar_label = AvatarWidget(
            role="me" if self.is_me else "other", 
            initial_path=self.avatar_path,
            avatar_size=40
        )
        self.setup_bubble(self.text)
        
        if self.is_me:
            self.chatbubble_layout.addStretch()
            self.chatbubble_layout.addWidget(self.bubble)
            self.chatbubble_layout.addWidget(self.avatar_label, alignment=Qt.AlignTop)
        else:
            self.chatbubble_layout.addWidget(self.avatar_label, alignment=Qt.AlignTop)
            self.chatbubble_layout.addWidget(self.bubble)
            self.chatbubble_layout.addStretch()
        
        """ 创建悬浮控制按钮 """
        self.btn_group = QFrame()
        self.btn_group.setFixedSize(300, 40)
        self.btn_group.setStyleSheet("""
            background: rgba(255,255,255,0.9);
            border-radius: 15px;
        """)
        self.btn_group.hide()
        # 按钮布局
        layout = QHBoxLayout(self.btn_group)
        layout.setContentsMargins(5, 0, 5, 0)
        # 操作按钮
        self.btn_up = self.setup_button("↑", "上移", "#4CAF50", layout)
        self.btn_down = self.setup_button("↓", "下移", "#2196F3", layout)
        self.btn_delete = self.setup_button("×", "删除", "#F44336", layout)
        self.btn_delete.clicked.connect(self.on_send_deleted)

        self.main_layout.addLayout(self.chatbubble_layout)
        self.main_layout.addWidget(self.btn_group, alignment=Qt.AlignHCenter)
        self.setLayout(self.main_layout)

    def setup_button(self, icon, text, color, parent_layout):
        """ 创建图标+文字的组合按钮 """
        btn_container = QWidget()  # 容器用于打包图标和文字
        btn_container.setFixedSize(100, 30)  # 总容量尺寸
        # 整体横向布局
        layout = QHBoxLayout(btn_container)
        layout.setContentsMargins(15, 0, 5, 0)
        layout.setSpacing(2)

        # -- 圆形图标部分 --
        icon_btn = QPushButton(icon)
        icon_btn.setFixedSize(28, 28)  # 圆形直径
        icon_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-radius: 14px;  /* 50%圆形 */
                background: {color};
                color: white;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {color}DD;  /* 悬加深色 */
            }}
        """)
        layout.addWidget(icon_btn)
        
        # -- 文字描述部分 --
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            QLabel {
                color: #666;
                font: 12px "Microsoft YaHei";
                margin-right: 5px;
            }
        """)
        layout.addWidget(text_label)
        
        # 传递点击事件（容器整体可点击）
        btn_container.mousePressEvent = lambda e: icon_btn.click()  
        parent_layout.addWidget(btn_container)
        
        return icon_btn  # 返回实际按钮用于信号连接

    def setup_bubble(self, text: str):
        """使用 QTextEdit 实现消息气泡"""      
        self.bubble = SmartTextEdit(text) 
        # self.bubble.setContentsMargins(0, 0, 0, 0)
        if self.is_me:
            self.bubble.setStyleSheet("""
                QTextEdit {
                    border: none;
                    border-radius: 10px;
                    padding: 8px;
                    padding-left: 12px;
                    background-color: #9EEA6A;  /* 绿色背景 */
                    color: #000;
                }
            """)
        else:
            self.bubble.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #ddd;  /* 细边框 */
                    border-radius: 10px;
                    padding: 8px;
                    padding-right: 12px;
                    background-color: #FFFFFF;  /* 白色背景 */
                    color: #000;
                }
            """)

    def setup_style(self):
        """设置微信风格的气泡和头像样式"""
        # 全局字体（根据系统字体调整）
        self.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei";
                font-size: 25px;
            }
        """)

    def enterEvent(self, event):
        """ 鼠标进入显示控制按钮 """
        self.btn_group.move(self.width()-110, 10)
        self.btn_group.show()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """ 鼠标离开隐藏按钮 """
        self.btn_group.hide()
        super().leaveEvent(event)
    
    def on_send_deleted(self):
        self.text_deleted.emit(self)

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
        self.setStyleSheet("""
            border-radius: 20px;
            border: 1px solid #eee;
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)

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

class SmartTextEdit(QTextEdit):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.initUI()
        self.setup_connections()

    def initUI(self): 
        # 设置尺寸策略（水平可扩展，垂直随内容变化）
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

         # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 按控件宽度自动换行
        self.setLineWrapMode(QTextBrowser.WidgetWidth)

        self.setMaximumWidth(300)
        self.padding = 10     # padding 调整
        self.max_width = 300  # 最大宽度
        # 设置初始文字
        self.setText(self.text)
        self.setReadOnly(True)
    
    def setup_connections(self):
        self.mouseDoubleClickEvent = self.enter_edit_mode
        self.focusOutEvent = self.exit_edit_mode
        self.keyPressEvent = self.editor_key_press_event
        self.textChanged.connect(self.update_size)
    
    def enter_edit_mode(self, event):
        self.setReadOnly(False)
    
    def exit_edit_mode(self, event):
        self.setReadOnly(True)
    
    def editor_key_press_event(self, event):
        """按回车键保存"""
        if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
            self.clearFocus()
        else:
            QTextEdit.keyPressEvent(self, event)

    def update_size(self, preedit_text=""):
        doc: QTextDocument = self.document()
        text = doc.toPlainText()
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(text) + font_metrics.width(preedit_text)
        # 限制最大宽度
        doc.setTextWidth(self.max_width - 12)

        content_width = min(text_width + 24, self.max_width)
        # 重新计算高度（基于设定的 textWidth）
        content_height = doc.size().height()

        # 更新控件尺寸
        self.setFixedWidth(int(content_width) + 12)
        self.setFixedHeight(int(content_height) + 12)

    def inputMethodEvent(self, event):
        super().inputMethodEvent(event)
        preedit_text = event.preeditString()

        self.update_size(preedit_text)  # 输入法拼音输入时也调整大小

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self.update_size)

class SmartTextBrowser(QTextBrowser):
    """根据文本内容自动调整大小的 QTextBrowser"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()

    def initUI(self): 
        # 设置尺寸策略（水平可扩展，垂直随内容变化）
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

         # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 按控件宽度自动换行
        self.setLineWrapMode(QTextBrowser.WidgetWidth)

        self.setMaximumWidth(300)
        # 允许打开外部链接
        self.setOpenExternalLinks(True)

    def update_size(self):
        doc: QTextDocument = self.document()
        max_text_width = self.maximumWidth() - 12

        ideal_width = doc.idealWidth()
        doc.setTextWidth(max_text_width)
        final_width = min(max_text_width, ideal_width)
        final_height = doc.size().height()

        # 设置控件大小，加入 padding
        self.setFixedWidth(int(final_width) + 24)
        self.setFixedHeight(int(final_height) + 16)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self.update_size)
