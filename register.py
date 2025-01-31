import sys
import pygame
from PyQt6 import QtWidgets
from login import Ui_LoginWindow
from menu import MenuApp


class LoginApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_register.clicked.connect(self.register)
        self.ui.pushButton_login.clicked.connect(self.login)

    def register(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        print(f"Регистрация: {username}, Пароль: {password}")

    def login(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        print(f"Вход: {username}, Пароль: {password}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
