import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import *
import database
import RecommendationWindow
from Singleton import SingletonDecorator, foo
from collaborative import Collaborative
import gui
from content import Content


def showRecommendation(window):
    window.changeLayout()
    window.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)


    rwindow = RecommendationWindow.RecommendationWindow()
    RecommendationWindow.foo['val'] = gui.foo['val'] = Collaborative(database.animes,database.ratings)
    RecommendationWindow.foo['cont'] = gui.foo['cont'] = Content(database.animes)
    RecommendationWindow.foo['user'] = gui.foo['user'] = database.user

    window = gui.MainWindow()
    window.go_to_recommendation.connect(lambda: showRecommendation(rwindow))
    rwindow.back_to_menu.connect(lambda: window.show())
    window.show()
    sys.exit(app.exec_())
