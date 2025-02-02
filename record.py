import sys
import sqlite3
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox


class ScoreboardApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица рекордов")
        self.setGeometry(100, 100, 600, 400)

        self.table_widget = QtWidgets.QTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Имя", "Счет"])

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('scores.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM scores ORDER BY score DESC')
        records = cursor.fetchall()

        self.table_widget.setRowCount(len(records))

        for row_index, (name, score) in enumerate(records):
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(name))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(str(score)))

        conn.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ScoreboardApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
