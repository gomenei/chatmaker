from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPlainTextEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QPropertyAnimation, QEasingCurve, QEvent
from ui.area.scroll import ScrollArea
from ui.area.input import InputArea
from ui.config import ConfigManager
from ui.widgets.status import StatusWidget
from ui.widgets.title import TitleWidget
from ui.area.emoji import EmojiArea
from ui.widgets.bubble import BubbleWidget

class ChatArea(QWidget):
    '''
    聊天组件:
        顶部状态栏
        标题栏
        消息展示区
        消息发送区
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.message_widgets = [] # 消息队列
        self.emoji_area_visible = False # 表情区域是否可见
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        # 主布局设置
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        # ===== 1. 手机状态栏 (全Emoji版本) =====
        self.status_bar = StatusWidget()
        # ===== 2. 微信风格标题栏 =====
        self.title_bar = TitleWidget("请输入昵称")
        # self.title_bar.back_clicked.connect(self.handle_back)
        # ===== 3. 原有聊天区域 =====
        self.scroll_area = ScrollArea(self)
        self.input_widget = InputArea()
        # ===== 4. emoji区域 =====
        self.emoji_area = EmojiArea()
        self.emoji_area.hide()
        
        # ===== 组合所有组件 =====
        self.main_layout.addWidget(self.status_bar)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.input_widget)
        self.main_layout.addWidget(self.emoji_area)
        
        # 设置布局伸缩权重
        self.main_layout.setStretch(0, 0)  # 状态栏
        self.main_layout.setStretch(1, 0)  # 标题栏
        self.main_layout.setStretch(2, 1)  # 消息区
        self.main_layout.setStretch(3, 0)  # 输入区
        self.main_layout.setStretch(4, 0)

    def setup_connections(self):
        # 连接发送信号与消息处理
        self.input_widget.send_clicked.connect(self.handle_send_message)
        self.input_widget.emoji_clicked.connect(self.toggle_emoji_area)
        self.input_widget.input_box.installEventFilter(self) # 监听输入框事件
        self.emoji_area.emoji_selected.connect(self.handle_emoji_input)

    def handle_send_message(self):
        """处理消息发送"""
        text = self.input_widget.input_box.toPlainText().strip()
        if not text:
            return
        
        self.scroll_area.add_message(text, True, self.config.get_avatar_path("me"))
        self.input_widget.input_box.clear() # 清空输入框
    
    def toggle_emoji_area(self):
        if self.emoji_area_visible:
            self.hide_emoji_area()
        else:
            self.show_emoji_area()
    
    def show_emoji_area(self):
        self.emoji_area_visible = True
        self.emoji_area.show()
        # 创建高度动画（操作emoji_area的高度）
        self.emoji_animation = QPropertyAnimation(self.emoji_area, b"maximumHeight")
        self.emoji_animation.setDuration(300)
        self.emoji_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # 从0开始展开
        self.emoji_animation.setStartValue(0)
        self.emoji_animation.setEndValue(200)  # 表情面板的最终高度
        
        # 注意：需要先设置emoji_area的初始高度
        self.emoji_area.setMaximumHeight(0)
        self.emoji_animation.start()

    def hide_emoji_area(self):
        """隐藏表情区域，伴随高度动画"""
        self.emoji_area_visible = False
        
        # 创建高度动画
        self.emoji_animation = QPropertyAnimation(self.emoji_area, b"maximumHeight")
        self.emoji_animation.setDuration(300)
        self.emoji_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # 从当前高度缩放到0
        self.emoji_animation.setStartValue(self.emoji_area.height())
        self.emoji_animation.setEndValue(0)
        
        # 动画结束时隐藏（通过信号连接）
        self.emoji_animation.finished.connect(lambda: self.emoji_area.hide())
        self.emoji_animation.start()
    
    def handle_emoji_input(self, emoji_code):
        last_focused = self.focusWidget()

        if last_focused is not None:
            if isinstance(last_focused, (QLineEdit, QTextEdit, QPlainTextEdit)):
                # 如果有选中的文本，先删除再插入
                last_focused.insert_emoji(emoji_code)
                # cursor = last_focused.textCursor()
                # cursor.insertText(emoji_code)
                # last_focused.setTextCursor(cursor)  # 确保光标位置正确
            else:
                print(f"当前焦点控件 {last_focused} 不支持插入文本")
        else:
            print("没有控件获得焦点")

    def eventFilter(self, obj, event):
        # === 拦截 FocusOut（仅当点击 emoji_btn/emoji_area 时）===
        if event.type() == QEvent.FocusOut:
            if (
                obj == self.input_widget.input_box  # 输入框
                or isinstance(obj, BubbleWidget)    # 消息气泡
            ):
                emoji_is_focus_stealer = (
                    self.input_widget.emoji_btn.underMouse()  # 点击表情按钮（判断来源）
                    or self.emoji_area.underMouse()           # 点击表情面板
                )
                if emoji_is_focus_stealer:
                    obj.setFocus()  # 重新获取焦点
                    return True     # 阻止 FocusOut
                
        # # === 处理 emoji_btn/emoji_area 点击 ===
        # if (obj == self.input_widget.emoji_btn or obj == self.emoji_area) and event.type() == QEvent.MouseButtonPress:
        #     print("emoji_btn/emoji_area clicked")
        #     last_focused = self.focusWidget()  # 记录当前焦点
        #     print(last_focused.text)
        #     QTimer.singleShot(0, lambda: last_focused.setFocus() if last_focused else None)
        #     return True  # 阻止事件传播
        return super().eventFilter(obj, event)

