from PyQt5.QtWidgets import QWidget, QPushButton, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class ClusterWidget(QWidget):
    def __init__(self, list_album: list, parent=None):
        super().__init__()
        self.parent = parent
        self.current_item_albums = None
        self.current_item_clusters = None
        self.list_album = list_album
        self.setFixedSize(QSize(660, 400))

        self.list_album_widget = QListWidget(self)

        self.list_album_widget.setStyleSheet(
            "QListWidget::item {"
            + "border-style: groove;"
            + "border-width:2px;"
            + "background-color: #DC143C;}"
            + "QListWidget::item:selected {"
            + "background-color: gray;}"
        )
        self.list_album_widget.move(10, 10)
        self.list_album_widget.itemClicked.connect(self.album_clicked)
        self.list_album_widget.resize(260, 385)
        self.init_list_album()

        self.clusters_list_album = []
        self.clusters_list_widget = QListWidget(self)
        self.clusters_list_widget.itemClicked.connect(self.cluster_clicked)
        self.clusters_list_widget.move(330, 10)
        self.clusters_list_widget.setStyleSheet(
            "QListWidget::item {"
            + "border-style: groove;"
            + "border-width:2px;"
            + "background-color: #00FA9A;}"
            + "QListWidget::item:"
            + "selected {"
            + "background-color: gray;}"
        )
        self.clusters_list_widget.resize(260, 385)

        btn_add_to_cluster = QPushButton(self)
        btn_add_to_cluster.setIcon(QIcon("image/right.png"))
        btn_add_to_cluster.setIconSize(QSize(40, 40))
        btn_add_to_cluster.move(275, 100)

        btn_add_to_cluster.clicked.connect(self.add_to_cluster_file)

        btn_add_all_to_cluster = QPushButton(self)
        btn_add_all_to_cluster.setIcon(QIcon("image/double_right.png"))
        btn_add_all_to_cluster.setIconSize(QSize(40, 40))
        btn_add_all_to_cluster.move(275, 150)
        btn_add_all_to_cluster.clicked.connect(self.add_all_to_cluster)

        del_cluster = QPushButton(self)
        del_cluster.setIcon(QIcon("image/del.png"))
        del_cluster.setIconSize(QSize(40, 40))
        del_cluster.move(275, 200)
        del_cluster.clicked.connect(self.del_cluster)

        btn_start_cluster = QPushButton(self)
        btn_start_cluster.setIcon(QIcon("image/cluster.png"))
        btn_start_cluster.setIconSize(QSize(40, 40))
        btn_start_cluster.move(600, 340)
        btn_start_cluster.clicked.connect(self.start_clustering)

    def start_clustering(self):
        self.parent.clusters_files(self.clusters_list_album)
        self.list_album.clear()
        self.list_album_widget.clear()
        self.clusters_list_album.clear()
        self.clusters_list_widget.clear()
        self.current_item_clusters = None
        self.current_item_albums = None
        self.close()

    def add_all_to_cluster(self):
        self.clusters_list_album = self.list_album
        self.refresh_cluster_widget()

    def add_to_cluster_file(self):
        if (
            self.current_item_albums
            and self.current_item_albums not in self.clusters_list_album
        ):
            self.clusters_list_album.append(self.current_item_albums)
            self.refresh_cluster_widget()

    def del_cluster(self):
        if self.current_item_clusters:
            self.clusters_list_album.remove(self.current_item_clusters)
            self.current_item_clusters = None
            self.refresh_cluster_widget()

    def refresh_cluster_widget(self):
        self.clusters_list_widget.clear()
        for i in self.clusters_list_album:
            self.clusters_list_widget.addItem(i)

    def album_clicked(self, item):
        self.current_item_albums = item.text()

    def cluster_clicked(self, item):
        self.current_item_clusters = item.text()

    def init_list_album(self):
        for album in self.list_album:
            self.list_album_widget.addItem(album)
