import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt,pyqtSignal
from PyQt5.QtGui import *
from SomeWidgets import Label,HBox,MyListWidget
import database

class DetailsWindow(QWidget):
    back_recommendation = pyqtSignal()
    def __init__(self, anime_name, content, collaborative,user):
        super(DetailsWindow,self).__init__()
        print(anime_name)
        self.anime_name =anime_name
        self.pic = QLabel()
        self.pixmap = QPixmap("covers/"+str(self.anime_name)+".jpg").scaled(147, 200)
        self.pic.setPixmap(self.pixmap)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.pic)
        hbox.addLayout(Form(self.anime_name,user))
        hbox.setAlignment(Qt.AlignLeft)
        vbox.addLayout(hbox)
        name = database.animes[database.animes['anime_id'] == int(anime_name)].iloc[0]['name']
        vbox.addWidget(Label("People who liked " + name + " also liked",20,True))

        vbox.addLayout(HBox(collaborative))

        vbox.addWidget(Label("Anime similar to " + name, 20,True))

        vbox.addLayout(HBox(content))
        self.setLayout(vbox)

    def clicked(self):
        print("apertou")


class Form(QFormLayout):
    def __init__(self,anime_name,user):
        super(Form,self).__init__()
        self.anime_name = anime_name
        self.user = user
        l = ['Name','Genre','Type','Episodes','Rating','Members']

        a = database.animes[database.animes['anime_id'] == int(anime_name)].iloc[0]

        for val in l:
            self.addRow(Label(val+':',15,True),Label(str(a[val.lower()]), 15,True))

        dic = {5:10, 4:9, 3:8, 2:7, 1:6, -1:5, -2:4, -3:3, -4:2, -5:1, 0:0}
        self.dic2 = {10:5, 9:4, 8:3, 7:2, 6:1, 5:-1, 4:-2,3:-3, 2:-4, 1:-5, 0:0}
        self.cb = QComboBox()
        self.cb.addItems(['-']+[str(i) for i in range(1,11)])
        self.cb.setCurrentIndex(dic[user.iloc[0][anime_name]])
        self.addRow(Label('Your Rating:',15,True), self.cb)
        self.cb.currentIndexChanged.connect(self.change)
    def change(self,i):
        self.user[self.anime_name] = self.dic2[i]

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = DetailsWindow('anime')

    window.show()
    sys.exit(app.exec_())
