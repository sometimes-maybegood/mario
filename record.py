import sys
import sqlite3
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox


class ScoreboardApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица рекордов")
        self.resize(400, 300)

        self.table_widget = QtWidgets.QTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Имя", "Счет"])
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('scores.db')
        cursor = conn.cursor()

        cursor.execute('SELECT name, score FROM scores ORDER BY score DESC')
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
    app.showFullScreen()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
