from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from ui.config import ConfigManager

class Pocket(QWidget):
    main_edited = pyqtSignal(str)
    status_edited = pyqtSignal(str)
    def __init__(self, is_me, pocket_type):
        super().__init__()
        self.is_me = is_me
        self.pocket_type = pocket_type
        self.config = ConfigManager().instance()
        self.init_ui()

    def init_ui(self):
        pocket_name = self.pocket_type + "_me" if self.is_me else self.pocket_type + "_other"
        pocket_path = self.config.get_pocket_path(pocket_name)
        self.pixmap = QPixmap(pocket_path)
        self.setFixedSize(self.pixmap.size())
        self.main_text = "恭喜发财，大吉大利" if "red_pocket" in self.pocket_type else "0.00"
        if self.pocket_type == "red_pocket_send":
            self.status_text = ""
            self.main_rect = QRect(65, 25, 150, 20)
            self.status_rect = QRect(0, 0, 0, 0)
        elif self.pocket_type == "red_pocket_receive":
            if self.is_me:
                self.status_text = "已被领完"
            else:
                self.status_text = "已领取"
            self.main_rect = QRect(65, 18, 150, 20)
            self.status_rect = QRect(65, 40, 120, 20)
        elif self.pocket_type == "transfer_send":
            if self.is_me:
                self.status_text = "你发起了一笔转账"
            else:
                self.status_text = "请收款"
            self.main_rect = QRect(66, 15, 150, 20)
            self.status_rect = QRect(57, 35, 120, 20)
        elif self.pocket_type == "transfer_receive":
            self.status_text = "已收款"
            self.main_rect = QRect(66, 15, 150, 20)
            self.status_rect = QRect(57, 35, 120, 20)

        self.main_line_edit = QLineEdit(self)
        self.main_line_edit.setGeometry(self.main_rect)
        self.main_line_edit.setText(self.main_text)
        self.main_line_edit.hide()
        self.main_line_edit.editingFinished.connect(self.main_finish)
        self.status_line_edit = QLineEdit(self)
        self.status_line_edit.setGeometry(self.status_rect)
        self.status_line_edit.setText(self.status_text)
        self.status_line_edit.hide()
        self.status_line_edit.editingFinished.connect(self.status_finish)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap.width(), self.pixmap.height(), self.pixmap)
        painter.setFont(QFont("HarmonyOS Sans SC Medium", 9))
        painter.setPen(Qt.white)
        painter.drawText(self.main_rect, Qt.AlignLeft, self.main_text)
        painter.setFont(QFont("黑体", 7))
        painter.drawText(self.status_rect, Qt.AlignLeft, self.status_text)

    def mouseDoubleClickEvent(self, event):
        if self.main_rect.contains(event.pos()):
            self.main_start()
        if self.status_rect.contains(event.pos()):
            self.status_start()

    def main_start(self):
        self.main_editing = True
        self.main_line_edit.setText(self.main_text)
        self.main_line_edit.show()
        self.main_line_edit.setFocus()

    def main_finish(self):
        self.main_editing = True
        self.main_text = self.main_line_edit.text()
        self.main_line_edit.hide()
        self.update()
        self.main_edited.emit(self.main_text)

    def status_start(self):
        self.status_editing = True
        self.status_line_edit.setText(self.status_text)
        self.status_line_edit.show()
        self.status_line_edit.setFocus()

    def status_finish(self):
        self.status_editing = True
        self.status_text = self.status_line_edit.text()
        self.status_line_edit.hide()
        self.update()
        self.status_edited.emit(self.main_text)
