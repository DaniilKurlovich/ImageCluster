from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsBlurEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class FullscreenViewerImage(QWidget):
    def __init__(self, path_to_image):
        super().__init__()
        self.image = QPixmap(path_to_image)
        self.setMinimumSize(800, 600)
        self.setGeometry(15, 15, 800, 600)
        self.background = QLabel(self)
        self.background.move(0, 0)
        self.back_pixmap = QPixmap(path_to_image)
        self.back_pixmap = self.back_pixmap.scaled(800, 600)
        self.background.setPixmap(self.back_pixmap)
        self.background.setAlignment(Qt.AlignCenter)
        blur = QGraphicsBlurEffect()
        self.background.setGraphicsEffect(blur)

        self.background.setAlignment(Qt.AlignCenter)

        self.label = QLabel(self)
        self.image = self.image.scaled(700, 500)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(self.image)
        self.label.resize(700, 500)

    def resizeEvent(self, e):
        self.background.move(self.width() // 2 - self.label.width() // 1.75,
                             self.height() // 2 - self.label.height() // 1.65)
        self.label.move(self.width() // 2 - self.label.width() // 2,
                        self.height() // 2 - self.label.height() // 2)
