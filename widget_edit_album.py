from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, \
                            QListWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class EditAlbum(QWidget):
    def __init__(self, name: str, list_images: list, parent=None):
        super().__init__()
        self.parent = parent

        self.name_folder = name

        self.current_item = None

        self.label = QLabel(self)
        self.label.setText('Input name photo album: ')
        self.label.move(15, 15)

        input_name = QLineEdit(self)
        input_name.setText(name)
        input_name.move(15, 40)
        input_name.resize(370, 30)
        input_name.textChanged[str].connect(self.on_changed)

        self.setFixedSize(400, 400)

        self.list_photo = list_images
        self.list_photo_widget = QListWidget(self)
        self.list_photo_widget.itemClicked.connect(self.click_on_photo)

        self.label_txt = QLabel(self)
        self.label_txt.setText('Path images: ')
        self.label_txt.move(15, 75)

        self.list_photo_widget.move(15, 95)
        self.list_photo_widget.resize(330, 225)

        add_path = QPushButton(self)
        add_path.resize(QSize(35, 35))
        add_path.setIconSize(QSize(55, 55))
        add_path.setIcon(QIcon('image/add.png'))
        add_path.move(350, 125)
        add_path.clicked.connect(self.add_photo)

        del_path = QPushButton(self)
        del_path.resize(QSize(35, 35))
        del_path.setIconSize(QSize(55, 55))
        del_path.setIcon(QIcon('image/del.png'))
        del_path.move(350, 250)
        del_path.clicked.connect(self.del_photo_from_list)

        create_album = QPushButton(self)
        create_album.move(310, 360)
        create_album.setText('Edit')
        create_album.clicked.connect(self.create_album)

        cancel = QPushButton(self)
        cancel.move(230, 360)
        cancel.setText('Cancel')
        cancel.clicked.connect(self.hide)

        self.reset_photo_widget()

    def create_album(self):
        if self.name_folder:
            if not self.parent.contain_name_album(self.name_folder):
                self.parent.create_album(self.name_folder, self.list_photo)
                self.close()
            else:
                QMessageBox.critical(None, 'Error', 'Name is taken')
        else:
            QMessageBox.critical(None, 'Error', 'Input name')

    def add_photo(self):
        url = QFileDialog.getOpenFileName(self, 'Open file', '/home',
                                          "Images (*.png *.bmp .jpg);")[0]
        if url:
            self.list_photo.append(url)
            self.reset_photo_widget()

    def click_on_photo(self, item):
        self.current_item = item.text()

    def del_photo_from_list(self):
        if self.current_item:
            self.list_photo.remove(self.current_item)
            self.reset_photo_widget()
            self.current_item = None

    def reset_photo_widget(self):
        self.list_photo_widget.clear()
        for i in self.list_photo:
            self.list_photo_widget.addItem(i)

    def on_changed(self, text):
        self.name_folder = text
