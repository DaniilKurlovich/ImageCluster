from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class SwitchButton(QPushButton):
    def __init__(self, icon_path, target_function, parent):
        super().__init__()
        self.target_function = target_function
        self.icon_path = icon_path
        self.setParent(parent)
        self.setMouseTracking(True)
        self.mode_clicked = False
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(50, 50))

    def mousePressEvent(self, e):
        if not self.mode_clicked:
            self.mode_clicked = True
        else:
            self.mode_clicked = False
        self.target_function()

    def mouseMoveEvent(self, event):

        if event.pos().x() > self.width()-10 or \
                event.pos().y() > self.height() - 10 or \
                event.pos().x() < 10 or event.pos().y() < 10:
            bmp = QIcon(self.icon_path)
            self.setIcon(bmp)

        else:
            if self.mode_clicked:
                bmp = QIcon('image/ok.png')
            else:
                bmp = QIcon('image/dis.png')

            self.setIcon(bmp)
        self.setIconSize(QSize(50, 50))
        return QPushButton.mouseMoveEvent(self, event)


class SearchWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setGeometry(50, 50, 450, 150)

        self.input_name = QLineEdit(self)
        self.input_name.move(10, 60)
        self.input_name.resize(370, 30)
        self.input_name.textChanged[str].connect(self.on_changed)

        self.flags = []

        self.album_mode = SwitchButton('image/album.png', self.set_album_mode,
                                       self)
        self.album_mode.move(9, 5)
        self.album_mode.resize(50, 50)

        self.current_name = ''

        self.folder_mode = SwitchButton('image/folder.png',
                                        self.set_folder_mode, self)
        self.folder_mode.move(60, 5)
        self.folder_mode.resize(50, 50)
        self.folder_mode.clicked.connect(self.set_folder_mode)

        btn_ok = QPushButton(self)
        btn_ok.setText('Find')
        btn_ok.move(400, 110)
        btn_ok.resize(40, 25)
        btn_ok.clicked.connect(self.find_files)

        btn_cancel = QPushButton(self)
        btn_cancel.setText('Cancel')
        btn_cancel.move(350, 110)
        btn_cancel.resize(40, 25)
        btn_cancel.clicked.connect(self.cancel)

        self.mode = ''

    def find_files(self):
        if not self.current_name:
            QMessageBox.critical(None, 'Error', 'Input name')
        elif not self.flags:
            QMessageBox.critical(None, 'Error', 'Input mode for search')
        else:
            self.parent.find_files(self.current_name, self.flags)
            self.cancel()

    def cancel(self):
        self.input_name.clear()
        self.current_name = ''
        self.flags = []
        self.folder_mode.mode_clicked = False
        self.album_mode.mode_clicked = False
        self.close()

    def set_folder_mode(self):
        if self.folder_mode.mode_clicked:
            self.flags.append('folder')
        else:
            self.flags.remove('folder')

    def set_album_mode(self):
        if self.album_mode.mode_clicked:
            self.flags.append('album')
        else:
            self.flags.remove('album')

    def on_changed(self, text):
        self.current_name = text
