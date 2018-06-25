import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt,pyqtSignal
from PyQt5.QtGui import *
from SomeWidgets import Label,HBox,MyListWidget
from DetailsWindow import DetailsWindow

import database
foo = {}

class VBox(QVBoxLayout):
    def __init__(self):
        super(VBox,self).__init__()
        self.details = None

    def add(self, anime_recommended, user_anime,content_anime, name):
        self.addWidget(Label("Animes with the same style that you liked:",20,True))
        self.addLayout(HBox(anime_recommended))
        self.addWidget(Label("Animes that people similar to you liked:",20,True))
        self.addLayout(HBox(user_anime))
        self.addWidget(Label("Animes similar to "+ name, 20,True))
        self.addLayout(HBox(content_anime))

    def add2(self, anime_name):
        print(anime_name)
        collaborative = foo['val'].get_similar_by_anime(str(anime_name),foo['user'], size=5)
        content = foo['cont'].get_similar_by_anime(anime_name, foo['user'],size=5)

        self.details = DetailsWindow(str(anime_name), collaborative, content,foo['user'])
        self.addWidget(self.details)


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
        self.button.setSizePolicy(10,10)

        self.vbox = VBox()
        hbox.addLayout(self.vbox)
        self.listWidget = MyListWidget()
        hbox.addWidget(self.listWidget)
        self.layout.addWidget(self.button)
        self.layout.addLayout(hbox)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.back_clicked)
        self.listWidget.itemClicked.connect(self.goToDetails)
        if(self.vbox.details is not None):
            self.vbox.details.button.clicked.connect(self.changeLayout)

    def goToDetails(self,item):
        self.vbox.clear()
        anime_id = database.animes[database.animes['name'] == item.text()].iloc[0]['anime_id']
        self.vbox.add2(anime_id)

    def changeLayout(self):
        anime_recommended = foo['cont'].get_similar_by_user(foo['user'],size=5)

        self.vbox.clear()
        item = self.listWidget.currentItem()
        if item is None:
            item = self.listWidget.item(0)

        anime_id = database.animes[database.animes['name'] == item.text()].iloc[0]['anime_id']

        anime_recommended2 = foo['val'].get_similar_by_user(foo['user'],size=5)
        print(anime_id)
        id, anime_recommended3 = foo['cont'].get_similar_by_most_ratings(foo['user'], size=5)

        name = database.animes[database.animes['anime_id'] == id].iloc[0]['name']
        self.vbox.add(anime_recommended, anime_recommended2, anime_recommended3, name)



    def back_clicked(self):
        self.back_to_menu.emit()
        self.hide()
