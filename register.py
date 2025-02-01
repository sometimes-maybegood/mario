import sys
import pygame
import sqlite3
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from login import Ui_LoginWindow
from menu import MenuApp


class LoginApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_register.clicked.connect(self.register)
        self.ui.pushButton_login.clicked.connect(self.login)
        self.current_user = None

    def show_error_message(self, title, message):
        error = QMessageBox()
        error.setWindowTitle(title)
        error.setText(message)
        error.setIcon(QMessageBox.Icon.Warning)
        error.setStandardButtons(QMessageBox.StandardButton.Ok)
        error.exec()

    def register(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()

        if not username or not password:
            self.show_error_message("Ошибка", "Логин и пароль не должны быть пустыми.")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            print(f"Регистрация успешна: {username}")
            self.current_user = username
            self.open_menu()
        except sqlite3.IntegrityError:
            self.show_error_message("Ошибка", "Пользователь с таким логином уже существует.")
        finally:
            conn.close()

    def login(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()

        if not username or not password:
            self.show_error_message("Ошибка", "Логин и пароль не должны быть пустыми.")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            print(f"Вход успешен: {username}")
            self.current_user = username
            self.open_menu()
        else:
            self.show_error_message("Ошибка", "Неверный логин или пароль.")

        conn.close()

    def open_menu(self):
        self.menu_window = MenuApp(current_user=self.current_user)
        self.menu_window.show()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
