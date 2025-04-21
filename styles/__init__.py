from PyQt5.QtCore import QFile, QTextStream

def load_style(file_path: str) -> str:
    """加载 QSS 文件并返回样式字符串"""
    style_file = QFile(file_path)
    if style_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(style_file)
        return stream.readAll()
    return ""