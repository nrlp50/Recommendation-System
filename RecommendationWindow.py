import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt,pyqtSignal
from PyQt5.QtGui import *
from SomeWidgets import Label,HBox,MyListWidget

import database
foo = {}

class VBox(QVBoxLayout):
    def __init__(self):
        super(VBox,self).__init__()


    def add(self, anime_recommended, user_anime,content_anime, name):
        self.addWidget(Label("Animes with the same style that you liked:",20,True))
        self.addLayout(HBox(anime_recommended))
        self.addWidget(Label("Animes that people similar to you liked:",20,True))
        self.addLayout(HBox(user_anime))
        self.addWidget(Label("Animes similar to "+name,20,True))
        self.addLayout(HBox(content_anime))

    def clear(self):
        while self.count():
            item = self.itemAt(0).widget()
            if item is not None:
                item.deleteLater()
            else:
                self.itemAt(0).clear()
            self.removeItem(self.itemAt(0))

class RecommendationWindow(QWidget):
    back_to_menu = pyqtSignal()
    def __init__(self):
        super(RecommendationWindow,self).__init__()
        self.layout = QVBoxLayout()

        hbox = QHBoxLayout()
        self.button = QPushButton("Back")
        self.button.setMinimumSize(self.button.minimumSizeHint())
        
        self.vbox = VBox()
        hbox.addLayout(self.vbox)
        self.listWidget = MyListWidget()
        hbox.addWidget(self.listWidget)
        self.layout.addWidget(self.button)
        self.layout.addLayout(hbox)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.back_clicked)
        self.listWidget.itemClicked.connect(self.changeLayout)

    def changeLayout(self):

        anime_recommended = foo['cont'].get_similar_by_user(foo['user'],size=5)

        self.vbox.clear()
        item = self.listWidget.currentItem()
        if item is None:
            item = self.listWidget.item(0)

        anime_id = database.animes[database.animes['name'] == item.text()].iloc[0]['anime_id']

        anime_recommended2 = foo['val'].get_similar_by_user(foo['user'],size=5)

        anime_recommended3 = foo['cont'].get_similar_by_anime(anime_id, size=5)


        self.vbox.add(anime_recommended, anime_recommended2, anime_recommended3, item.text())


    def back_clicked(self):

        self.back_to_menu.emit()
        self.hide()
