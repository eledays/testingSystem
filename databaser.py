import sqlite3
import csv


class Databaser:

    def __init__(self, filename='tests.db'):

        self.connection = sqlite3.connect(filename, check_same_thread=False)
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
        r = self.cursor.fetchone()

        return r[0] if r is not None else None

    def get_questions(self, test_id):
        self.cursor.execute('''SELECT value FROM questions WHERE test_id = ?''', (test_id,))
        return list(map(lambda x: x[0], self.cursor.fetchall()))

    def get_answers(self, test_id):
        self.cursor.execute('''SELECT value FROM answers WHERE test_id = ?''', (test_id,))
        return list(map(lambda x: x[0], self.cursor.fetchall()))

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


def clear_str(s):
    return s.replace('"', '\'').replace(';', ',').lower().replace('ё', 'е').strip()


class Filer:

    def save_answers(self, answers, db, test_id, filename='answers.csv'):
        answers = [clear_str(e) for e in answers]
        right_answers = [clear_str(e) for e in db.get_answers(test_id)]

        with open(filename, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"')

            for i, (a, r) in enumerate(zip(answers, right_answers)):
                writer.writerow([i, a, r == a])


if __name__ == '__main__':
    f = Filer()
    f.save_answers(['absd;"fg1', 'a42'])