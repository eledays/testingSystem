from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QHeaderView, QErrorMessage, QRadioButton, QLabel, QLineEdit, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

from PIL import Image, ImageDraw, ImageFont

from databaser import Databaser, Filer

import sys


db = Databaser()
filer = Filer()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)
        self.setWindowTitle('Тестовая система')
        self.initUI()

        self.second_window = None

    def initUI(self):
        self.create_btn.clicked.connect(self.create_test)
        self.edit_btn.clicked.connect(self.edit_test)
        self.do_btn.clicked.connect(self.do_test)
        self.stat_btn.clicked.connect(self.view_statistics)
        self.import_btn.clicked.connect(self.import_test)
        self.export_btn.clicked.connect(self.export_test)

    def do_test(self):
        self.second_window = ChoiceTestWindow()
        self.second_window.show()

    def create_test(self):
        self.second_window = CreateWindow()
        self.second_window.show()

    def edit_test(self):
        print('Редактирование теста')

    def view_statistics(self):
        print('Просмотр статистики')

    def import_test(self):
        print('Импорт тестов')

    def export_test(self):
        print('Экспорт тестов')


class CreateWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi('create.ui', self)
        self.setWindowTitle('Создание теста')
        self.initUI()

        self.qs = []
        self.error = QErrorMessage()

    def initUI(self):
        self.add_btn.clicked.connect(self.add_question)
        self.finish_btn.clicked.connect(self.finish)
        self.table.setHorizontalHeaderLabels(['Вопрос', 'Правильный ответ'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def add_question(self):
        # TODO Добавить вопросы с вариантами ответов

        q, ok_pressed = QInputDialog.getText(self, 'Создание вопроса', 'Введите вопрос')
        if not ok_pressed:
            return

        a, ok_pressed = QInputDialog.getText(self, 'Создание вопроса', f'Введите ответ на вопрос "{q}"')
        if not ok_pressed:
            return

        self.qs.append((q, a))
        self.table.setRowCount(len(self.qs))
        self.table.setItem(len(self.qs) - 1, 0, QTableWidgetItem(q))
        self.table.setItem(len(self.qs) - 1, 1, QTableWidgetItem(a))

    def finish(self):
        if self.name.text().strip() and self.qs:
            db.create_test(self.name.text(), self.qs)
            self.close()
            return
        elif not self.name.text().strip():
            self.error.showMessage('Название теста не может быть пустым')
        elif not self.qs:
            self.error.showMessage('Тест должен содержать хотя бы один вопрос')


class ChoiceTestWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi('choice_test.ui', self)
        self.setWindowTitle('Выбор теста')
        self.initUI()

    def initUI(self):
        tests = db.get_test_names()

        self.test_btns = []
        for i, test in enumerate(tests):
            self.test_btns.append(QRadioButton(test[0], parent=self.groupBox))
            self.test_btns[-1].move(25, i * 25 + 25)
            self.test_btns[-1].toggled.connect(self.select_test)

        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_test)

    def select_test(self):
        self.start_btn.setEnabled(True)

    def start_test(self):
        test_name = list(filter(lambda x: x.toggled, self.test_btns))[0].text()
        test_id = db.get_test_id(test_name)
        self.second_window = TestWindow(test_id)
        self.second_window.show()
        self.close()


class TestWindow(QMainWindow):

    def __init__(self, test_id):

        self.test_id = test_id
        self.test_name = db.get_test_name(self.test_id)
        self.qs = db.get_questions(self.test_id)

        self.question_labels = []
        self.question_line_edits = []

        super().__init__()

        uic.loadUi('test.ui', self)
        self.setWindowTitle(f'Тест "{self.test_name}"')
        self.initUI()

    def initUI(self):
        for i, q in enumerate(self.qs):
            self.question_labels.append(QLabel(f'{i + 1}. {q}', self))
            self.question_line_edits.append(QLineEdit(self))

            self.question_labels[-1].setContentsMargins(0, 0, 15, 0)

            hb = QHBoxLayout(self)
            hb.addWidget(self.question_labels[-1])
            hb.addWidget(self.question_line_edits[-1])

            hb.setContentsMargins(0, 15, 0, 0)

            self.verticalLayout.addLayout(hb)

        self.finish_btn.clicked.connect(self.finish_test)

    def finish_test(self):
        answers = [x.text() for x in self.question_line_edits]
        filer.save_answers(answers, db, self.test_id)

        self.close()
        self.second_window = ResultWindow()
        self.second_window.show()


class ResultWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi('result.ui', self)

        self.setWindowTitle('Результат теста')
        self.setMaximumSize(500, 500)
        self.setMinimumSize(500, 500)

        self.initUI()

    def initUI(self):
        make_result_image()

        self.pixmap = QPixmap('result.png')

        self.img_lbl.setPixmap(self.pixmap)


def make_result_image(right_count, all_count):
    img = Image.new('RGBA', (500, 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('Roboto.ttf', 20)

    draw.text((200, 150), 'Результат теста', font=myFont, fill=(255, 255, 255, 255))

    draw.rectangle((200, 150, 300, 350), fill=(255, 255, 255, 255))
    img.save('result.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
