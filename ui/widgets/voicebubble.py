from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QPixmap, QTransform
import os


class VoiceBubbleWidget(QWidget):
    def __init__(self, duration=0, icon_path="fig/icon/voicemessage.png", is_me=True, parent=None, mode="voice"): 
        super().__init__(parent)
        self.is_me = is_me

        self.icon_label = QLabel()
        abs_path = os.path.abspath(icon_path)
        pixmap = QPixmap(abs_path)
        if is_me:
            pixmap = pixmap.transformed(QTransform().scale(-1, 1))
        self.icon_label.setPixmap(pixmap.scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_label.setFixedSize(28, 22)
        self.icon_label.setStyleSheet("margin-right:6px;")

        if mode == "voice":
            self.duration_edit = QLineEdit(f"{duration}″")
        else:
            self.duration_edit = QLineEdit(f"通话时长 {duration}{duration}:{duration}{duration}/已取消/对方无应答/对方已拒绝")
        self.duration_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.duration_edit.textChanged.connect(self.update_bubble_size)
        self.duration_edit.setStyleSheet("""
                border:none;
                background:transparent;
                font-size: 18px;
            """)
        self.duration_edit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.duration_edit.setReadOnly(True)  # 初始不可编辑
        self.duration_edit.installEventFilter(self)  # 监听双击
        self.duration_edit.focusOutEvent = self.make_readonly_on_focus_out
        self.duration_edit.keyPressEvent = self.handle_return_to_finish_edit

        layout = QHBoxLayout(self)
        if is_me and mode == "voice":
            layout.setContentsMargins(35, 6, 6, 6)
        elif mode == "voice":
            layout.setContentsMargins(6, 6, 35, 6)
        else:
            layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(2)

        if is_me:
            layout.addWidget(self.duration_edit)
            layout.addWidget(self.icon_label)  
        else:
            layout.addWidget(self.icon_label)  
            layout.addWidget(self.duration_edit)
        layout.addStretch()

        color = "#9EEA6A" if self.is_me else "#FFFFFF"
        self.setStyleSheet(f"""
            background: {color};
            border-radius: 10px;
            border: none;
        """)

        self.setObjectName("bubble_me" if is_me else "bubble_other")
        self.setContentsMargins(6, 6, 6, 6)
        self.setMinimumHeight(32)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        QTimer.singleShot(0, self.update_bubble_size)


    def set_duration(self, value):
        self.duration_edit.setText(f"{value}″")
        self.update_bubble_size()

    def get_duration(self):
        try:
            return int(self.duration_edit.text().replace("″", ""))
        except ValueError:
            return 0

    def compute_text_width(self, text):
        """根据文字长度动态计算 QLineEdit 宽度"""
        font_metrics = self.duration_edit.fontMetrics()
        text_width = font_metrics.width(text)
        return text_width + 4  # 最少30，留白+光标

    def update_bubble_size(self):
        """根据当前文本更新 QLineEdit 和整个气泡宽度"""
        
        self.duration_edit.setFixedWidth(self.compute_text_width(self.duration_edit.text()))
        self.updateGeometry() 
    
    def eventFilter(self, obj, event):
        if obj == self.duration_edit and event.type() == QEvent.MouseButtonDblClick:
            self.duration_edit.setReadOnly(False)  # 双击进入编辑模式
            self.duration_edit.setFocus()
        return super().eventFilter(obj, event)
    
    def make_readonly_on_focus_out(self, event):
        self.duration_edit.setReadOnly(True)
        QLineEdit.focusOutEvent(self.duration_edit, event)

    def handle_return_to_finish_edit(self, event):
        if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
            self.duration_edit.clearFocus()  # 会触发失焦 -> 只读
        else:
            QLineEdit.keyPressEvent(self.duration_edit, event)


