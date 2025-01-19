from PyQt6 import QtCore, QtGui, QtWidgets
import sys


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(400, 300)

        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(0, 0, 400, 300)
        self.background.setPixmap(QtGui.QPixmap("background.jpg"))
        self.background.setScaledContents(True)

        self.lineEdit_username = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_username.setGeometry(QtCore.QRect(100, 100, 200, 30))
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_username.setPlaceholderText("Логин")
        self.lineEdit_username.setStyleSheet("padding: 5px; border-radius: 10px; border: 2px solid #ffffff;")

        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(100, 150, 200, 30))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setPlaceholderText("Пароль")
        self.lineEdit_password.setStyleSheet("padding: 5px; border-radius: 10px; border: 2px solid #ffffff;")

        self.pushButton_register = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_register.setGeometry(QtCore.QRect(100, 200, 90, 34))
        self.pushButton_register.setObjectName("pushButton_register")
        self.pushButton_register.setStyleSheet("""
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

        self.pushButton_login = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_login.setGeometry(QtCore.QRect(210, 200, 90, 34))
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_login.setStyleSheet("""
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

        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.pushButton_register.setText(_translate("LoginWindow", "Регистрация"))
        self.pushButton_login.setText(_translate("LoginWindow", "Вход"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec())