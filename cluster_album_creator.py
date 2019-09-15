from PyQt5.QtWidgets import QWidget, QListWidget, QGridLayout, \
                            QListWidgetItem, QLabel, QScrollArea, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QSize, Qt


class ClusterSelector(QWidget):
    def __init__(self, parent, image_tegs):
        '''
        :param image_tegs: dict with (name image - key):(value:
                           list[path_image, list_tegs])
        '''
        super().__init__()

        self.parent = parent

        self.grid = QGridLayout()
        self.grid_possible_album_buttons = QGridLayout()
        self.lower_grid = QGridLayout()

        self.added_albums = {}

        self.path_image = {}
        self.image_dict = image_tegs

        self.image = None
        self.possible_cluster = None
        self.scroll = QScrollArea()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter)
        self.scroll.setWidget(self.label)
        self.scroll.setWidgetResizable(True)

        self.label_list_images = QLabel()
        self.label_list_images.setText('Clustering images: ')
        self.list_images = QListWidget()
        self.list_images.itemClicked.connect(self.item_clicked)
        self.list_images.setFixedWidth(160)

        self.grid_images_and_text = QGridLayout()
        self.grid_images_and_text.addWidget(self.label_list_images, 0, 0)
        self.grid_images_and_text.addWidget(self.list_images, 1, 0)

        self.add_album = QPushButton()
        self.add_album.setFixedSize(QSize(40, 40))
        self.add_album.setText('Add')
        self.add_album.clicked.connect(self._add_album)

        self.del_album = QPushButton()
        self.del_album.setFixedSize(QSize(40, 40))
        self.del_album.setText('Del')
        self.del_album.clicked.connect(self._del_album)

        self.grid_buttons_manage = QGridLayout()
        self.grid_buttons_manage.addWidget(self.add_album, 0, 0)
        self.grid_buttons_manage.addWidget(self.del_album, 1, 0)

        self.label_tags = QLabel()
        self.label_tags.setText('Tags')
        self.list_tags = QListWidget()
        self.list_tags.setFixedHeight(130)

        self.accept_album = QPushButton()
        self.accept_album.setFixedSize(40, 40)
        self.accept_album.setIconSize(QSize(40, 40))
        self.accept_album.setIcon(QIcon('image/ok.png'))
        self.accept_album.clicked.connect(self.accept_albums)

        self.grid_tags = QGridLayout()
        self.grid_tags.addWidget(self.label_tags, 0, 0)
        self.grid_tags.addWidget(self.list_tags, 1, 0)
        self.grid_tags.addWidget(self.accept_album, 1, 1)

        for image in image_tegs:
            item_widget = QListWidgetItem(image)
            item_widget.setIcon(QIcon(image_tegs[image][0]))
            self.path_image[image] = image_tegs[image][0]
            self.list_images.addItem(item_widget)

        self.cluster_dict = {}
        self.label_album = QLabel()
        self.label_album.setText('Choose cluster album ')
        self.list_possible_cluster_album = QListWidget()
        self.list_possible_cluster_album.setFixedHeight(130)
        self.list_possible_cluster_album.itemClicked.connect(
                                                     self.show_images)
        self.grid_cluster = QGridLayout()
        self.grid_cluster.addWidget(self.label_album, 0, 0)
        self.grid_cluster.addWidget(self.list_possible_cluster_album, 1, 0)

        self.init_cluster_album()

        self.grid_image_and_list = QGridLayout()
        self.grid_image_and_list.addLayout(self.grid_images_and_text, 0, 0)
        self.grid_image_and_list.addWidget(self.scroll, 0, 1)

        self.grid.addLayout(self.grid_image_and_list, 0, 0)
        self.grid_possible_album_buttons.addLayout(self.grid_cluster, 0, 0)
        self.grid_possible_album_buttons.addLayout(self.grid_buttons_manage,
                                                   0, 1)
        self.lower_grid.addLayout(self.grid_possible_album_buttons, 0, 0)
        self.lower_grid.addLayout(self.grid_tags, 0, 1)
        self.grid.addLayout(self.lower_grid, 1, 0)
        self.grid.setRowStretch(0, 3)
        self.setLayout(self.grid)

    def accept_albums(self):
        self.parent.add_cluster_albums(self.added_albums)
        self.close()

    def _add_album(self):
        if self.possible_cluster:
            if self.possible_cluster not in self.added_albums:
                self.added_albums[self.possible_cluster] = \
                        self.get_list_tegs_of_cluster(self.possible_cluster)
                self.init_cluster_album()

    def get_list_tegs_of_cluster(self, cluster):
        return self.cluster_dict[cluster]

    def _del_album(self):
        if self.possible_cluster:
            if self.possible_cluster in self.added_albums:
                self.added_albums.pop(self.possible_cluster)
                self.possible_cluster = None
                self.init_cluster_album()

    def show_images(self, item):
        self.possible_cluster = item.text()
        item = item.text()
        self.list_images.clear()
        for image in self.image_dict:
            item_widget = QListWidgetItem(image)
            item_widget.setIcon(QIcon(self.image_dict[image][0]))
            if image in self.cluster_dict[item]:
                item_widget.setBackground(QColor('#00FF7F'))
            else:
                item_widget.setBackground(QColor('#FA8072'))
            self.path_image[image] = self.image_dict[image][0]
            self.list_images.addItem(item_widget)

    def init_cluster_album(self):
        self.list_possible_cluster_album.clear()
        for name in self.image_dict:
            for cluster in self.image_dict[name][1]:
                if cluster not in self.cluster_dict:
                    self.cluster_dict[cluster] = [name, self.path_image[name]]
                else:
                    if name not in self.cluster_dict[cluster]:
                        self.cluster_dict[cluster].append([name,
                                                          self.path_image[
                                                              name]])
        for key in self.cluster_dict:
            item = QListWidgetItem(key)
            if key in self.added_albums:
                item.setBackground(QColor('#00FF7F'))
            self.list_possible_cluster_album.addItem(item)

    def reset_list_tags_widget(self):
        self.list_tags.clear()
        for list_tags in self.image_dict[self.image][1]:
            self.list_tags.addItem(QListWidgetItem(list_tags))

    def resizeEvent(self, e):
        size = e.size()
        self.label.resize(size.width() - 100, size.height() - 100)
        self.resize(size)

    def item_clicked(self, item):
        self.image = item.text()
        self.reset_list_tags_widget()
        self.label.setPixmap(QPixmap(self.path_image[self.image]))
        self.label.resize(QPixmap(self.path_image[self.image]).size())
        self.update()
