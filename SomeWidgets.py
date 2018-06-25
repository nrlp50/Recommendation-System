import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import *
import database



class MyListWidget(QListWidget):
    def __init__(self):
        super(MyListWidget,self).__init__()
        top_animes = database.animes
        for i in range(database.animes.shape[0]):
            self.addItem(top_animes.iloc[i]['name'])


class Label(QLabel):
    def __init__(self,text,size,bold):
        super(Label,self).__init__()
        self.setText(text)
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        self.setFont(font)

class HBox(QHBoxLayout):
    def __init__(self, anime_list):
        super(HBox,self).__init__()

        self.setContentsMargins(0,0,0,0)
        for i in anime_list:
            self.addWidget(Animes(i))

    def clear(self):
        while self.count():
            item = self.itemAt(0).widget().deleteLater()
            self.removeItem(self.itemAt(0))

class Animes(QLabel):
    def __init__(self, anime_name):
        super(Animes,self).__init__()
        self.anime_name = anime_name

        self.pixmap = QPixmap("covers/"+str(self.anime_name)+".jpg").scaled(147, 200)
        self.setPixmap(self.pixmap)
