import sys
import pygame
from PyQt6 import QtWidgets
from menu_qt import Ui_MenuWindow
from level1 import st


class MenuApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MenuWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_record.clicked.connect(self.record)

    def start(self):
        st()

    def record(self):
        exec(open('record.py').read())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
