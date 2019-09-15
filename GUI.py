import sys
import os
import re
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QApplication,\
                            QListWidget, QListWidgetItem, QListView, \
                            QFileSystemModel, QTreeView, QVBoxLayout, \
                            QHBoxLayout, QTabWidget, QMessageBox

from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import QSize, Qt, QDir

from widget_add_album import AddAlbum
from widget_edit_album import EditAlbum
from view_image import FullscreenViewerImage
from search_widget import SearchWidget
from cluster_selector_widget import ClusterWidget
from classificator import get_tags_image
from cluster_album_creator import ClusterSelector


class PhotoAlbumAndDirectoryViewer(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.setFixedWidth(400)
        self.layout = QVBoxLayout(self)

        # Инициализация вкладок
        self.tabs = QTabWidget()

        # init first tab
        self.directory_viewer = QTreeView()

        self.cur_item = None

        path = QDir.rootPath()
        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)

        self.directory_viewer.setModel(self.dirModel)
        self.directory_viewer.setRootIndex(self.dirModel.index(path))

        self.directory_viewer.clicked.connect(self.parent.on_clicked_directory)

        self.tabs.addTab(self.directory_viewer, 'Directory')

        # init photo album creator and viewer
        self.album_viewer = QListWidget()

        self.dict_albums = {}    # key - name album, value list path photo path

        self.album_viewer.setViewMode(QListWidget.IconMode)
        self.album_viewer.setResizeMode(QListWidget.Adjust)
        self.album_viewer.setMovement(QListView.Static)

        self.tabs.addTab(self.album_viewer, 'Album viewer')

        self.album_viewer.itemClicked.connect(self.on_clicked_album)

        self.layout.addWidget(self.tabs)

        # init btn for manage photo album directory

        self.search_btn = QPushButton(self)
        self.search_btn.resize(QSize(28, 28))
        self.search_btn.setIconSize(QSize(28, 28))
        self.search_btn.setIcon(QIcon('image/search.png'))
        self.search_btn.clicked.connect(self.open_find_widget)

        self.add_album = QPushButton(self)
        self.add_album.resize(QSize(28, 28))
        self.add_album.setIconSize(QSize(28, 28))
        self.add_album.setIcon(QIcon('image/add_album.png'))
        self.add_album.clicked.connect(self.add_album_widget)

        self.edit_album = QPushButton(self)
        self.edit_album.resize(QSize(28, 28))
        self.edit_album.setIconSize(QSize(40, 44))
        self.edit_album.setIcon(QIcon('image/edit_folder.png'))
        self.edit_album.clicked.connect(self.edit_album_f)

        self.del_album = QPushButton(self)
        self.del_album.resize(QSize(28, 28))
        self.del_album.setIconSize(QSize(28, 28))
        self.del_album.setIcon(QIcon('image/delete_folder.png'))
        self.del_album.clicked.connect(self.del_album_f)

        self.cluster_widget = ClusterWidget(list(self.dict_albums.keys()),
                                            parent=self)

        self.btn_cluster = QPushButton(self)
        self.btn_cluster.resize(QSize(28, 28))
        self.btn_cluster.setIconSize(QSize(28, 28))
        self.btn_cluster.setIcon(QIcon('image/cluster.png'))
        self.btn_cluster.clicked.connect(self.show_cluster_widget)

        # init widgets edit and add, del album

        self.add_album_w = AddAlbum(self)
        self.edit_album_w = None

        self.search_widget = SearchWidget(self)
        self.cluster_creator = None

        self.setLayout(self.layout)

    def show_cluster_widget(self):
        self.cluster_widget = ClusterWidget(list(self.dict_albums.keys()),
                                            parent=self)
        self.cluster_widget.show()

    def clusters_files(self, clusters_list_album):
        dict_tags = {}
        for album in clusters_list_album:
            for image_path in self.dict_albums[album]:
                print('Dict_tags: ', dict_tags)
                dict_tags[DirectoryViewer.get_name_from_path(image_path)] = \
                    [image_path, list(get_tags_image(image_path).keys())]

        self.cluster_creator = ClusterSelector(self, dict_tags)
        self.cluster_creator.show()

    def open_find_widget(self):
        self.search_widget.show()

    def add_cluster_albums(self, added_albums):
        del self.cluster_creator
        for i in added_albums:
            self.create_album(i, [added_albums[i][1]])

    def find_files(self, file_name, flags_search: list):
        if 'folder' in flags_search:
            self.search_file_in_folders(file_name)
        if 'album' in flags_search:
            self.search_file_in_album(file_name)

    def search_file_in_folders(self, file_name):
        pass

    def search_file_in_album(self, file_name):
        list_equal = []
        for file_list in self.dict_albums:
            for file_path in self.dict_albums[file_list]:
                print(file_path, ':', file_name)
                if file_name == DirectoryViewer.get_name_from_path(file_path):
                    list_equal.append(file_path)
        if not list_equal:
            QMessageBox.critical(None, 'Error', 'No files found in album')
        else:
            self.parent.change_list(list_equal)

    def del_album_f(self):
        if self.cur_item:
            if self.cur_item in self.dict_albums:
                self.dict_albums.pop(self.cur_item)
                self.update_album_list()

    def edit_album_f(self):
        if self.cur_item:
            if self.cur_item in self.dict_albums:
                self.edit_album_w = EditAlbum(name=self.cur_item,
                                              list_images=self.dict_albums[
                                                  self.cur_item],
                                              parent=self)
                self.edit_album_w.show()

    def contain_name_album(self, name):
        if name in self.dict_albums:
            return True
        return False

    def create_album(self, name, photo_list):
        if name in self.dict_albums:
            self.dict_albums[name].extend(photo_list)
        else:
            self.dict_albums[name] = photo_list

        self.album_viewer.clear()
        for i in self.dict_albums:
            item = QListWidgetItem()
            item.setText(i)
            item.setIcon(QIcon('image/photo.png'))
            item.setSizeHint(QSize(128, 128))
            self.album_viewer.addItem(item)
            item.setTextAlignment(Qt.AlignCenter)

    def update_album_list(self):
        self.album_viewer.clear()
        for i in self.dict_albums:
            item = QListWidgetItem()
            item.setText(i)
            item.setIcon(QIcon('image/photo.png'))
            item.setSizeHint(QSize(128, 128))
            self.album_viewer.addItem(item)
            item.setTextAlignment(Qt.AlignCenter)

    def add_album_widget(self):
        self.add_album_w.show()

    def resizeEvent(self, e):
        cor = e.size()
        self.btn_cluster.move(self.tabs.width() - 165, 0)
        self.search_btn.move(self.tabs.width() - 130, 0)
        self.add_album.move(self.tabs.width() - 25, 0)
        self.edit_album.move(self.tabs.width() - 60, 0)
        self.del_album.move(self.tabs.width() - 95, 0)
        self.tabs.resize(abs(cor.width() - self.tabs.width()),
                         abs(cor.height() - self.tabs.height()))

    def on_clicked_album(self, item):
        self.cur_item = item.text()
        text_item = item.text()
        self.parent.on_clicked_album(self.dict_albums[text_item])


class DirectoryViewer(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.set_design()
        self.list_of_folder = []
        self.parent = parent
        hlay = QHBoxLayout(self)

        self.album_and_dir_viewer = PhotoAlbumAndDirectoryViewer(self)

        self.show_image_w = None

        self.listview = QListWidget()
        self.listview.setViewMode(QListWidget.IconMode)
        self.listview.setResizeMode(QListWidget.Adjust)
        self.listview.setMovement(QListView.Static)
        self.listview.itemDoubleClicked.connect(self.show_image)

        hlay.addWidget(self.album_and_dir_viewer)
        hlay.addWidget(self.listview)

    def set_design(self):
        self.setStyleSheet("alternate-background-color: #C0C0C0;"
                           "background: #808080;"
                           "border-color: #C0C0C0;")

    def show_image(self, image):
        for i in self.list_of_folder:
            if self.get_name_from_path(i) == image.text():
                self.show_image_w = FullscreenViewerImage(i)
                self.show_image_w.show()

    @staticmethod
    def is_image(image_path):
        mime_type = re.search(r'\.(\w+)$', image_path)
        if mime_type:
            if mime_type.group() in ['.png', '.jpeg', '.bmp']:
                return True
        return False

    @staticmethod
    def get_name_from_path(path):
        s = re.search(r'[^/]*\.(\w+)$', path)
        if s:
            return s.group()
        return path

    def reset_list_view(self):
        self.listview.clear()
        for i in self.list_of_folder:
            item = QListWidgetItem()
            item.setSizeHint(QSize(128, 128))
            item.setIcon(QIcon(i))
            item.setText(self.get_name_from_path(i))
            self.listview.addItem(item)
            item.setTextAlignment(Qt.AlignCenter)

    def on_clicked_album(self, array_images_path):
        self.list_of_folder = []
        for file in array_images_path:
            self.list_of_folder.append(file)
        self.reset_list_view()

    def change_list(self, list):
        self.list_of_folder = list
        self.reset_list_view()

    def on_clicked_directory(self, index):
        path = self.album_and_dir_viewer.dirModel.fileInfo(index)\
                                        .absoluteFilePath()
        self.list_of_folder = []
        for file in os.listdir(path):
            if DirectoryViewer.is_image(file):
                self.list_of_folder.append(path + '/' + file)
        self.reset_list_view()


class PathAndAlbumAndImageViewer(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_directory_widget()

    def init_directory_widget(self):
        self.model = QFileSystemModel()
        self.model.setRootPath('C')

        self.tree = DirectoryViewer(self)
        self.tree.setWindowTitle("Dir View")
        self.tree.resize(640, 480)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)


class PhotoViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_design_color()

        self.setWindowTitle('Photo Viewer v1.0')
        self.setGeometry(50, 50, 900, 900)
        self.central_widget = PathAndAlbumAndImageViewer(self)
        self.setGeometry(50, 50, 850, 850)
        self.setCentralWidget(self.central_widget)

    def set_design_color(self):
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor("#696969"))
        pal.setColor(QPalette.WindowText, Qt.white)
        pal.setColor(QPalette.Base, QColor(25, 25, 25))
        pal.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        pal.setColor(QPalette.ToolTipBase, Qt.white)
        pal.setColor(QPalette.ToolTipText, Qt.white)
        pal.setColor(QPalette.Text, Qt.white)
        pal.setColor(QPalette.Button, QColor(53, 53, 53))
        pal.setColor(QPalette.ButtonText, Qt.white)
        pal.setColor(QPalette.BrightText, Qt.white)
        pal.setColor(QPalette.Link, QColor(42, 130, 218))
        pal.setColor(QPalette.Highlight, QColor(42, 130, 218))
        pal.setColor(QPalette.HighlightedText, Qt.black)

        self.setPalette(pal)

    def resizeEvent(self, event):
        size = event.size()
        self.central_widget.move(25, 25)
        self.resize(size.width(), size.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhotoViewer()
    window.show()
    sys.exit(app.exec_())
