from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, QSize

class ImageAndGifWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)  # 图片居中显示
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    def set_image(self, file_path, max_size=200):
        pixmap = QPixmap(file_path)
        
        if not pixmap.isNull():
            # 保持宽高比自动缩放，不超过max_size
            scaled_pixmap = pixmap.scaled(
                max_size, 
                max_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)
            return True
        return False

    def set_gif(self, file_path, max_size=200):
        self.movie = QMovie(file_path)
        if not self.movie.isValid():
            return False
        
        self.movie.setScaledSize(QSize(max_size, max_size))
        self.label.setMovie(self.movie)
        self.movie.start()
        return True