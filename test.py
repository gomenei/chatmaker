from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QSizeF
from PyQt5.QtGui import QFont, QTextOption

class WeChatInput(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setupStyle()
        self.setupBehavior()

    def initUI(self):
        """初始化界面设置"""
        self.setPlaceholderText("请输入消息")                # 占位文字
        self.setFont(QFont("Microsoft YaHei UI", 10))      # 默认字体
        self.setMinimumHeight(40)                          # 最小高度
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 滚动条策略
        
        # 推荐优化设置
        self.setAcceptRichText(False)                     # 禁用富文本
        self.setLineWrapMode(QTextEdit.WidgetWidth)       # 自动换行
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)  # 智能换行

    def setupStyle(self):
        """设置微信风格样式"""
        style = """
        QTextEdit {
            border: 1px solid #e5e5e5;
            border-radius: 4px;
            padding: 8px 12px;
            font-family: Microsoft YaHei UI, PingFang SC, Helvetica Neue, Hiragino Sans GB;
            font-size: 14px;
            color: #333333;
            selection-background-color: #b3d9e6;
            min-height: 40px;
            max-height: 120px;
        }
        
        QTextEdit:focus {
            border: 1px solid #07c160;
        }
        
        QScrollBar:vertical {
            border: none;
            background: white;
            width: 8px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background: #cccccc;
            min-height: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }
        """
        self.setStyleSheet(style)

    def setupBehavior(self):
        """设置动态高度调整"""
        self.document().documentLayout().documentSizeChanged.connect(
            lambda size: self.adjustHeight(size)
        )

    def adjustHeight(self, size: QSizeF):
        """自动调整输入框高度"""
        new_height = max(40, min(int(size.height()) + 10, 120))
        self.setFixedHeight(new_height)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    
    mainWin = QWidget()
    layout = QVBoxLayout()
    input_box = WeChatInput()
    
    layout.addWidget(input_box)
    mainWin.setLayout(layout)
    mainWin.resize(300, 200)
    mainWin.show()
    
    sys.exit(app.exec_())
