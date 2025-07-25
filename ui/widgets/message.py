from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy,
                             QPushButton, QLabel, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QTime, QTimer
from PyQt5.QtGui import QPixmap, QTextOption, QTextCursor
from ..config import ConfigManager
from ui.widgets.avatar import AvatarWidget
from ui.widgets.bubble import BubbleWidget, VoiceBubbleWidget
from ui.widgets.pocket import Pocket
from ui.widgets.photo_gif import ImageAndGifWidget


class MessageWidget(QWidget):
    """带头像的消息气泡组件，支持双向显示和内容编辑"""
    text_edited = pyqtSignal(str)  # 内容修改信号
    text_deleted = pyqtSignal(QWidget)
    text_up = pyqtSignal(QWidget)
    text_down = pyqtSignal(QWidget)

    def __init__(self, text: str, is_me: bool, role: str, avatar_path: str, parent, message_type = "text"):
        super().__init__(parent)
        self.is_me = is_me  # 消息方向标识
        self.role = role  # 群成员标识
        self.avatar_path = avatar_path
        self.text_content = text
        self.message_type = message_type
        self.config = ConfigManager().instance()
        self.refuse = False
        self.init_ui()
        self.load_style()

    def init_ui(self):
        """初始化界面布局"""
        self.parent_width = self.parent().width()
        self.setup_avatar()
        self.setup_bubble(self.text_content)
        self.setup_button()

        """主布局设置"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # 优化边距

        """气泡 + 头像设置"""
        self.chatbubble_layout = QHBoxLayout()
        self.chatbubble_layout.setContentsMargins(0, 0, 0, 0)
        if self.message_type == "system":
            self.chatbubble_layout.addStretch()
            self.chatbubble_layout.addWidget(self.bubble_container, alignment=Qt.AlignCenter)
            self.chatbubble_layout.addStretch()
        else:
            if self.is_me:
                self.chatbubble_layout.addStretch()
                self.chatbubble_layout.addWidget(self.bubble_container)
                self.chatbubble_layout.addWidget(self.avatar_label, alignment=Qt.AlignTop)
            else:
                self.chatbubble_layout.addWidget(self.avatar_label, alignment=Qt.AlignTop)
                self.chatbubble_layout.addWidget(self.bubble_container)
                self.chatbubble_layout.addStretch()

        self.main_layout.addLayout(self.chatbubble_layout)
        self.main_layout.addWidget(self.btn_group, alignment=Qt.AlignHCenter)
        self.setLayout(self.main_layout)

    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/message.qss"))

    def setup_avatar(self):
        avatar_width = int(self.parent_width / 10)
        self.avatar_label = AvatarWidget(
            role="me" if self.is_me else "other",
            initial_path=self.avatar_path,
            avatar_size=avatar_width
        )

    def setup_button(self):
        """ 创建悬浮控制按钮 """
        self.btn_group = QFrame()
        self.btn_group.setObjectName("btn_group")
        self.btn_group.hide()
        btn_group_width = int(self.parent_width * (5 / 9))
        btn_group_height = int(self.parent_width * (1 / 14))
        self.btn_group.setFixedSize(btn_group_width, btn_group_height)

        # 按钮布局
        layout = QHBoxLayout(self.btn_group)
        layout.setContentsMargins(0, 0, 0, 0)
        # 操作按钮
        self.btn_up = self.setup_signal_button("↑", "上移", "btn_up", layout)
        self.btn_down = self.setup_signal_button("↓", "下移", "btn_down", layout)
        self.btn_delete = self.setup_signal_button("×", "删除", "btn_delete", layout)
        if self.message_type != "system" and self.is_me:
            self.btn_refuse = self.setup_signal_button("!", "拒收", "btn_refuse", layout)

        self.btn_delete.clicked.connect(lambda: self.text_deleted.emit(self))
        self.btn_down.clicked.connect(lambda: self.text_down.emit(self))
        self.btn_up.clicked.connect(lambda: self.text_up.emit(self))
        if self.message_type != "system" and self.is_me:
            self.btn_refuse.clicked.connect(self.toggle_refuse)

    def setup_signal_button(self, icon, text, btn_name, parent_layout):
        """ 创建图标+文字的组合按钮 """
        btn_container = QWidget()  # 容器用于打包图标和文字
        btn_container.setObjectName("btn_container")
        # 整体横向布局
        layout = QHBoxLayout(btn_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # -- 圆形图标部分 --
        icon_btn = QPushButton(icon)
        icon_btn.setObjectName(btn_name)
        icon_btn_size = int(self.parent_width / 20)
        icon_btn.setFixedSize(icon_btn_size, icon_btn_size)  # 圆形直径
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
        """使用 Widget 实现带三角的消息气泡"""
        # 创建容器
        self.bubble_container = QWidget()
        self.bubble_container.setObjectName("bubble_container_me" if self.is_me else "bubble_container_other")
        is_bubble = False
        if self.text_content == "pocket":
            self.bubble = Pocket(self.is_me, self.message_type)
            self.bubble.setObjectName("bubble_me" if self.is_me else "bubble_other")
        # 气泡主体
        elif self.message_type == "voice":
            self.bubble = VoiceBubbleWidget(duration=0, icon_path="fig/icon/voicemessage_other.png", is_me=self.is_me, mode=self.message_type)
            is_bubble = True
        elif self.message_type == "voicecall":
            self.bubble = VoiceBubbleWidget(duration=0, icon_path="fig/icon/voicecall.png", is_me=self.is_me, mode=self.message_type)
            is_bubble = True
        elif self.message_type == "videocall":
            self.bubble = VoiceBubbleWidget(duration=0, icon_path="fig/icon/videocall.png", is_me=self.is_me, mode=self.message_type)
            is_bubble = True
        elif self.message_type == "photo":
            self.bubble = ImageAndGifWidget()
            self.bubble.set_image(text)
        elif self.message_type == "gif":
            self.bubble = ImageAndGifWidget()
            self.bubble.set_gif(text)
        else:
            self.bubble = BubbleWidget(text, self)
            is_bubble = True

        self.bubble.setObjectName("bubble_me" if self.is_me else "bubble_other")
        self.refuse_icon = QLabel()
        self.refuse_icon.setObjectName("refuse")
        refuse_pic = QPixmap(self.config.get_refuse_icon())
        refuse_pic = refuse_pic.scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.refuse_icon.setPixmap(refuse_pic)

        self.triangle_label = QLabel()
        self.triangle_label.setObjectName("triangle_me" if self.is_me else "triangle_other")
        self.triangle_label.setFixedSize(12, 20)

        # 容器布局设置
        container_layout = QHBoxLayout(self.bubble_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        if self.is_me:
            container_layout.addWidget(self.refuse_icon, alignment=Qt.AlignRight)
            container_layout.addWidget(self.bubble, alignment=Qt.AlignRight)
            
            if is_bubble:
                self.triangle_label.setStyleSheet("margin-left: -2px;")
                container_layout.addWidget(self.triangle_label, alignment=Qt.AlignTop)
        else:
            if is_bubble:
                self.triangle_label.setStyleSheet("margin-right: -1px;")
                container_layout.addWidget(self.triangle_label, alignment=Qt.AlignTop)
            container_layout.addWidget(self.bubble, stretch=1, alignment=Qt.AlignLeft)

        self.refuse_icon.setVisible(False)

    def toggle_refuse(self):
        self.refuse = not self.refuse
        self.refuse_icon.setVisible(self.refuse)

    def enterEvent(self, event):
        """ 鼠标进入显示控制按钮 """
        self.btn_group.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """ 鼠标离开隐藏按钮 """
        self.btn_group.hide()
        super().leaveEvent(event)

class SystemMessageWidget(MessageWidget):
    def __init__(self, is_me=True, mode="time", target_name="对方", parent=None):
        self.mode = mode
        self.target_name = target_name
        self.edit = None
        self.bubble_container = QWidget() 
        super().__init__(
            text="", is_me=is_me, role="", avatar_path="", parent=parent, message_type="system"
        )
        default_text = self._default_text()
        self.setup_bubble(default_text)
        self.bubble = self.bubble_container
        self.avatar_label.hide()
        self.triangle_label = QWidget()  # 防止父类逻辑访问时报错
        self.triangle_label.hide()

    def _default_text(self):
        sender = "你" if self.is_me else self.target_name
        receiver = self.target_name if self.is_me else "你"

        if self.mode == "time":
            return QTime.currentTime().toString("HH:mm")
        elif self.mode == "tickle":
            sender = "我" if self.is_me else self.target_name
            receiver = self.target_name if self.is_me else "我"
            return f"{sender}拍了拍{receiver}"
        elif self.mode == "red envelope":
            icon_path = "fig/icon/red_envelope.svg"
            icon_img = f'<img src="{icon_path}" width="18" height="20" style="vertical-align: top; margin-right:2px;">'
            return f"{icon_img} {sender}领取了{receiver}的<span style=\"color: #DAA520;\">红包</span>"
        elif self.mode == "withdraw":
            return f"{sender}撤回了一条消息"
        elif self.mode == "transfer":
            return "收款方24小时内未接收你的<span style=\"color:dodgerblue;\">转账</span>，已过期"
        return ""
    
    def setup_bubble(self, default_text: str):
        layout = self.bubble_container.layout()
        if layout is None:
            layout = QHBoxLayout()
            self.bubble_container.setLayout(layout)
        else:
            # 清空旧布局内容（防止重复添加）
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)

        self.bubble_container.setObjectName("bubble_container_system")
        layout.setContentsMargins(0, 6, 0, 6)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        if self.mode == "transfer":
            self.edit = QLabel()
            self.edit.setText(self._default_text())
            self.edit.setTextFormat(Qt.RichText)
            self.edit.setStyleSheet(
                "border: none; background: transparent; font-size: 16px; color: gray;" 
            )
            self.edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            content_layout.addWidget(self.edit, 0, Qt.AlignVCenter)
        else:
            self.edit = SystemBubbleWidget(text=default_text)
            self.edit.setStyleSheet(
                "border: none; background: transparent; font-size: 15px; color: gray;" \
                "padding: 0px; margin: 0px;"
            )
            self.edit.setAlignment(Qt.AlignCenter)
            content_layout.addWidget(self.edit)
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        layout.addStretch()
        layout.addWidget(content_widget)
        layout.addStretch()

    def text(self):
        if isinstance(self.edit, QTextEdit):
            return self.edit.toPlainText()
        elif isinstance(self.edit, QLabel):
            return self.edit.text()
        return ""
    
class SystemBubbleWidget(QTextEdit):
    text_edited = pyqtSignal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setHtml(text)
        self.setReadOnly(True)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(24)
        self._last_text = text

        # 事件覆盖
        self.mouseDoubleClickEvent = self.enter_edit_mode
        self.focusOutEvent = self.exit_edit_mode
        self.keyPressEvent = self.editor_key_press_event

    def enter_edit_mode(self, event):
        self.setReadOnly(False)
        self.setStyleSheet("background:white; border:1px solid gray; color:black; font-size:15px;")
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        self.setFocus()

    def exit_edit_mode(self, event):
        self.setReadOnly(True)
        self.setStyleSheet("background:transparent; border:none; color:gray; font-size:15px;")
        new_text = self.toPlainText()
        if new_text != self._last_text:
            self._last_text = new_text
            self.text_edited.emit(new_text)

    def editor_key_press_event(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not (event.modifiers() & Qt.ShiftModifier):
            self.clearFocus()
        else:
            QTextEdit.keyPressEvent(self, event)
