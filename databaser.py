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

        self.connection.commit()

    def add_question(self, test_id, value):
        self.cursor.execute('''INSERT INTO questions (test_id, value) VALUES (?, ?)''', (test_id, value))
        self.connection.commit()

    def add_answer(self, test_id, value):
        self.cursor.execute('''INSERT INTO answers (test_id, value) VALUES (?, ?)''', (test_id, value))
        self.connection.commit()

    def get_test_name(self, test_id):
        self.cursor.execute('''SELECT name FROM tests WHERE id = ?''', (test_id,))
        return self.cursor.fetchone()[0]

    def get_test_id(self, name):
        self.cursor.execute('''SELECT id FROM tests WHERE name = ?''', (name,))
        return self.cursor.fetchone()[0]

    def get_questions(self, test_id):
        self.cursor.execute('''SELECT value FROM questions WHERE test_id = ?''', (test_id,))
        return self.cursor.fetchall()

    def get_answers(self, test_id):
        self.cursor.execute('''SELECT value FROM answers WHERE test_id = ?''', (test_id,))
        return self.cursor.fetchall()

    def get_test_names(self):
        self.cursor.execute('''SELECT name FROM tests''')
        return self.cursor.fetchall()

    def create_test(self, name, qs):
        self.cursor.execute('''INSERT INTO tests (name) VALUES (?)''', (name,))
        self.connection.commit()

        test_id = self.get_test_id(name)
        for q, a in qs:
            self.add_question(test_id, q)
            self.add_answer(test_id, a)

        self.connection.commit()
