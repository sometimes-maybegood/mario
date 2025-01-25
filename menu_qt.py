from PyQt6 import QtCore, QtGui, QtWidgets
import sys



class Ui_MenuWindow(object):
    def setupUi(self, MenuWindow):
        MenuWindow.setObjectName("MenuWindow")
        MenuWindow.resize(400, 300)

        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(0, 0, 400, 300)
        self.background.setPixmap(QtGui.QPixmap("background.jpg"))
        self.background.setScaledContents(True)

        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(100, 120, 200, 40))
        self.pushButton_start.setObjectName("pushButton_start")
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
        self.pushButton_record.setGeometry(QtCore.QRect(130, 180, 140, 30))
        self.pushButton_record.setObjectName("pushButton_record")
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

        MenuWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MenuWindow)
        QtCore.QMetaObject.connectSlotsByName(MenuWindow)

    def retranslateUi(self, MenuWindow):
        _translate = QtCore.QCoreApplication.translate
        MenuWindow.setWindowTitle(_translate("MenuWindow", "Menu"))
        self.pushButton_start.setText(_translate("MenuWindow", "Начать игру"))
        self.pushButton_record.setText(_translate("MenuWindow", "Рекорд"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_MenuWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec())