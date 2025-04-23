from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QLabel
from PyQt5.QtGui import QFont, QCursor, QPixmap
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QTimer, QEvent, QRect

class ExpandButton(QPushButton):
    button_clicked = pyqtSignal(str)

    def __init__(self, text: str, button_texts: list = None, panel_size: tuple = None):
        super().__init__(text)
        self.button_texts = button_texts
        self.panel_size = panel_size
        self.init_ui()
        self.load_style()
    
    def init_ui(self):
        self.setObjectName("ExpandButton")
        # 创建面板内容
        if self.panel_size:

            self.setup_panel()
        
            # 定时器优化
            self.hide_timer = QTimer()
            self.hide_timer.setSingleShot(True)
            self.hide_timer.timeout.connect(self.panel.hide)
    
    def load_style(self):
        from styles import load_style
        self.setStyleSheet(load_style("styles/expand_button.qss"))
        
    def setup_panel(self):
        self.panel = QWidget(flags=Qt.ToolTip)
        self.panel.setObjectName("expand_panel")
        self.panel.setFixedSize(*self.panel_size)

        self.panel_layout = QVBoxLayout(self.panel)
        self.panel_layout.setSpacing(0)          # 按钮间垂直间距设为0
        self.panel_layout.setContentsMargins(0, 0, 0, 0)  # 移除布局与面板边缘的边距
        for button_line in self.button_texts:
            layout = QHBoxLayout()
            for button in button_line:
                self.add_button(button, "./fig/fix.png", layout)
            self.panel_layout.addLayout(layout)

        self.panel.installEventFilter(self)

    def add_button(self, text, icon_path, parent_layout):
        widget = QWidget()
        widget.setMaximumHeight(100)
        widget.setMaximumWidth(100)
        widget.setObjectName("custom_btn")  # 为整体设置标识符（用于样式表）
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除布局边距
        layout.setSpacing(0)                # 移除组件间距

        icon = QLabel()
        icon.setAlignment(Qt.AlignCenter)
        icon.setPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio))

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(icon)
        layout.addWidget(label)
        widget.mousePressEvent = lambda _: self.button_clicked.emit(text)
        parent_layout.addWidget(widget)

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.panel_size:
            self.hide_timer.stop()
            self.update_panel_position()
            self.panel.show()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.panel_size:
            self.hide_timer.start(50)  # 统一延迟隐藏逻辑

    def update_panel_position(self):
        """动态更新面板位置以适应窗口移动"""
        button_rect = self.rect()
        global_pos = self.mapToGlobal(QPoint(0, 0))
        
        # 计算垂直居中位置
        panel_y = global_pos.y() + (button_rect.height() - self.panel.height()) // 2
        # 计算最上方位置
        panel_y = global_pos.y() + (button_rect.height() - self.panel.height()) 
        # 计算最下方位置
        panel_y = global_pos.y()
        self.panel.move(global_pos.x() - self.panel.width(), panel_y)

    def eventFilter(self, obj, event):
        if self.panel_size:
            if obj == self.panel:
                if event.type() == QEvent.Enter:
                    self.setProperty("hover", "true")
                    self.style().polish(self)
                    self.hide_timer.stop()
                elif event.type() == QEvent.Leave:
                    # 检查是否进入主按钮区域
                    self.setProperty("hover", "false")
                    self.style().polish(self)
                    cursor_pos = QCursor.pos()
                    button_global_rect = QRect(
                        self.mapToGlobal(QPoint(0, 0)),
                        self.size()
                    )
                    if not button_global_rect.contains(cursor_pos):
                        self.hide_timer.start(50)
        return super().eventFilter(obj, event)