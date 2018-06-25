import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt,pyqtSignal
from PyQt5.QtGui import *
from SomeWidgets import Label,HBox,MyListWidget

class DetailsWindow(QWidget):
    def __init__(self,anime_name):
        super(DetailsWindow,self).__init__()
        hbox = QHBoxLayout()
        hbox.addWidget(Window(anime_name))
        self.lw = MyListWidget()

        hbox.addWidget(self.lw)
        self.setLayout(hbox)



class Window(QWidget):
    back_recommendation = pyqtSignal()
    def __init__(self, anime_name):
        super(Window,self).__init__()
        self.anime_name =anime_name
        self.button = QPushButton("Back")
        self.button.setSizePolicy(10,10)
        self.button.clicked.connect(self.clicked)
        self.pic = QLabel()
        self.pixmap = QPixmap(self.anime_name+".jpg").scaled(147, 200)
        self.pic.setPixmap(self.pixmap)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.pic)
        hbox.addLayout(Form(self.anime_name))
        hbox.setAlignment(Qt.AlignLeft)
        vbox.addWidget(self.button)
        vbox.addLayout(hbox)
        vbox.addWidget(Label("People who liked Megalo box also liked",20,True))
        vbox.addLayout(HBox(['anime','anime','anime','anime','anime']))
        vbox.addWidget(Label("Anime similar to Megalo box",20,True))
        vbox.addLayout(HBox(['anime','anime','anime','anime','anime']))
        self.setLayout(vbox)
    def clicked(self):
        print("apertou")
        # self.back_recommendation.emit()
        # self.hide()


class Form(QFormLayout):
    def __init__(self,anime_name):
        super(Form,self).__init__()
        l = ['Information','Name','Rating','Episodes','Genre','Type','Members']
        for i in l:
            self.addRow(Label(i+':',15,True),Label('oi',15,True))



if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = DetailsWindow('anime')

    window.show()
    sys.exit(app.exec_())
