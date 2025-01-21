from PyQt6 import QtCore, QtGui, QtWidgets
import sys



class Ui_MenuWindow(object):
    def setupUi(self, MenuWindow):
        MenuWindow.setObjectName("MenuWindow")
        MenuWindow.resize(800, 800)

        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 800)
        self.background.setPixmap(QtGui.QPixmap("background.png"))
        self.background.setScaledContents(True)

        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(350, 250, 300, 80))
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_start.setPlaceholderText("Начать игру")
        self.pushButton_start.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50; /* Зеленый фон */
                        color: white; /* Белый текст */
                        border-radius: 10px; /* Закругленные углы */
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #45a049; /* Темно-зеленый при наведении */
                    }
                """)

        self.pushButton_record = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_record.setGeometry(QtCore.QRect(350, 250, 200, 60))
        self.pushButton_record.setObjectName("pushButton_record")
        self.pushButton_record.setPlaceholderText("Рекорд")
        self.pushButton_record.setStyleSheet("""
                    QPushButton {
                        background-color: #008CBA; /* Синий фон */
                        color: white; /* Белый текст */
                        border-radius: 10px; /* Закругленные углы */
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #007B9E; /* Темно-синий при наведении */
                    }
                """)



