import sqlite3


class Databaser:

    def __init__(self, filename='tests.db'):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY,
            name TEXT
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            test_id INTEGER,
            value TEXT
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY,
            test_id INTEGER,
            value TEXT
        )''')
