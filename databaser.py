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
        r = self.cursor.fetchone()
        return r[0] if r is not None else None

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

    def get_qas(self, test_id):
        questions = self.get_questions(test_id)
        answers = self.get_answers(test_id)
        return list(zip(questions, answers))

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

    def edit_test(self, test_id, name, qs):
        self.cursor.execute('''DELETE FROM questions WHERE test_id = ?''', (test_id,))
        self.cursor.execute('''DELETE FROM answers WHERE test_id = ?''', (test_id,))
        self.cursor.execute('''DELETE FROM tests WHERE id = ?''', (test_id,))
        self.connection.commit()
        self.create_test(name, qs)

    def export_test(self, test_id):
        name = f'{self.get_test_name(test_id).replace(" ", "_")}.csv'

        with open(name, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"')
            questions = self.get_questions(test_id)
            answers = self.get_answers(test_id)

            for i, q in enumerate(questions):
                writer.writerow([q, answers[i]])

        return name

    def import_test(self, filename):
        with open(filename, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')
            reader = list(reader)
            while [] in reader:
                reader.remove([])

            test_name = filename.replace('_', ' ').rstrip('.csv').split('/')[-1]
            if self.get_test_id(test_name) is None:
                self.create_test(test_name, reader)
            else:
                self.create_test(test_name + ' Копия', reader)


def clear_str(s):
    return s.replace('"', '\'').replace(';', ',').lower().replace('ё', 'е').strip()


class Filer:

    def save_answers(self, answers, db, test_id, filename='sources/answers.csv'):
        answers = [clear_str(e) for e in answers]
        right_answers = [clear_str(e) for e in db.get_answers(test_id)]

        with open(filename, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"')
            for i, (a, r) in enumerate(zip(answers, right_answers)):
                writer.writerow([i, a, int(r == a)])

        with open(f'results/{test_id}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"')
            for i, (a, r) in enumerate(zip(answers, right_answers)):
                writer.writerow([i, a, int(r == a)])

    def __call__(self, filename='answers.csv'):
        with open(filename, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')
            reader = list(reader)
            while [] in reader:
                reader.remove([])
            return reader

    def get_right_all_count(self, test_id=None):
        reader = self(f'results/{test_id}.csv' if test_id is not None else 'sources/answers.csv')
        return sum(map(lambda x: int(x[2]), reader)), len(reader)


if __name__ == '__main__':
    f = Filer()
    f.save_answers(['absd;"fg1', 'a42'])