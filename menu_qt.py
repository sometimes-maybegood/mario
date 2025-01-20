from PyQt6 import QtCore, QtGui, QtWidgets
import sys


class Ui_MenuWindow(object):
    def setupUi(self, MenuWindow):
        MenuWindow.setObjectName("MenuWindow")
        MenuWindow.resize(800, 800)

        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(0, 0, 800, 800)
        self.background.setPixmap(QtGui.QPixmap("background.jpg"))
        self.background.setScaledContents(True)

        self.lineEdit_start = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_start.setGeometry(QtCore.QRect(100, 100, 200, 30))
        self.lineEdit_start.setObjectName("lineEdit_start")
        self.lineEdit_start.setPlaceholderText("Начать")

