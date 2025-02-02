import sqlite3


def create_database():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
