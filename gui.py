import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import *
import database
from collaborative import Collaborative

foo = {}

anime_list = [1535, 1254, 16498, 527, 11757, 249, 5114, 20, 30276,
232, 1575, 813, 7674, 550, 32281, 552, 11061, 530, 21, 199, 1614]

class Window(QWidget):
    def __init__(self, anime_id,anime_name):
        super(Window,self).__init__()
        self.anime_id = anime_id
        self.anime_name = anime_name
        self.pic = QLabel()

        self.pixmap = QPixmap("covers/"+self.anime_id+".jpg").scaled(147, 200)
        self.pic.setPixmap(self.pixmap)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5,5,5,5)
        self.resize(self.pixmap.width(),self.pixmap.height())
        self.cb = QComboBox()
        self.cb.addItems(['-']+[str(i) for i in range(0,11)])
        self.layout.addWidget(self.pic)
        self.layout.addWidget(self.cb)
        self.setLayout(self.layout)



class GridWindow(QWidget):
    def __init__(self):
        super(GridWindow,self).__init__()
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0,0,0,0)


        # top_animes = database.animes.set_index('anime_id',drop=True).loc[anime_list].reset_index()
        top_animes = database.animes.iloc[:21]
        for i in range(1,4):
            for j in range(1,8):
                row = top_animes.iloc[(i-1)*7 + j-1] # erro
                w = Window(str(row['anime_id']),row['name'])
                self.grid.addWidget(w,i,j)


        self.setLayout(self.grid)

    def getAllWidgets(self):
        ret = []
        for i in reversed(range(self.grid.count())):
            item = self.grid.takeAt(i)
            item = item.widget()
            anime_name = item.anime_name
            anime_id = item.anime_id
            score = item.cb.currentText()
            score = score if score != '-' else 5
            ret.append((anime_id,anime_name,int(score)))
        return ret


class MainWindow(QWidget):
    go_to_recommendation = pyqtSignal()
    def __init__(self):
        super(MainWindow,self).__init__()

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        label = QLabel("Before we begin, we need to know a bit before a bit about you! Classify the animes below")
        font = label.font()
        font.setPointSize(30)
        font.setBold(True)
        label.setFont(font)

        hbox.addWidget(label)
        self.button = QPushButton("OK")

        hbox.addWidget(self.button)
        vbox.addLayout(hbox)
        self.grid = GridWindow()
        vbox.addWidget(self.grid)
        self.setLayout(vbox)
        self.button.clicked.connect(self.clicked)

    def clicked(self):

        classified_animes = self.grid.getAllWidgets()

        # print(len(foo['user'].columns))
        for i in classified_animes:
            foo['user'][str(i[0])] = i[2]
            # print(i[0],i[2])


        foo['val'].process(foo['user'])


        self.go_to_recommendation.emit()
        self.hide()
