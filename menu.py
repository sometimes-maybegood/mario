import sys
import pygame
from PyQt6 import QtWidgets
from menu_qt import Ui_MenuWindow
from level1 import st
from record import ScoreboardApp


class MenuApp(QtWidgets.QMainWindow):
    def __init__(self, current_user=None):
        super().__init__()
        self.ui = Ui_MenuWindow()
        self.ui.setupUi(self)
        self.current_user = current_user
        with open('user.txt', 'w') as f:
            f.write(str(self.current_user))
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_record.clicked.connect(self.record)

    def start(self):
        st()
        pygame.quit()

    def record(self):
        self.menu_window = ScoreboardApp()
        self.menu_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MenuApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
