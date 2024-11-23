import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QHeaderView, QErrorMessage, QRadioButton, QLabel, QLineEdit, QHBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

from PIL import Image, ImageDraw, ImageFont

from databaser import Databaser, Filer

import sys


db = Databaser()
filer = Filer()


# Основное окно приложения
class MainWindow(QMainWindow):
    """Основное окно приложения."""

    def __init__(self):
        """Инициализация основного окна приложения."""

        super().__init__()

        # Загрузка интерфейса из файла
        uic.loadUi('uis/main.ui', self)
        self.setWindowTitle('Тестовая система')
        self.initUI()

        self.second_window = None

    def initUI(self):
        """Инициализация интерфейса основного окна приложения."""

        self.create_btn.clicked.connect(self.create_test)
        self.edit_btn.clicked.connect(self.edit_test)
        self.do_btn.clicked.connect(self.do_test)
        self.stat_btn.clicked.connect(self.view_statistics)
        self.import_btn.clicked.connect(self.import_test)
        self.export_btn.clicked.connect(self.export_test)

        self.logo = QPixmap(os.path.join('sources', 'logo.png'))
        self.logo = self.logo.scaled(500, int(500 * self.logo.height() / self.logo.width()))
        self.label.setPixmap(self.logo)

    def do_test(self):
        """Открывает окно выбора теста для прохождения."""

        self.second_window = ChoiceTestWindow(ChoiceTestWindow.DO_TEST)
        self.second_window.show()

    def create_test(self):
        """Открывает окно для создания нового теста."""

        self.second_window = CreateWindow()
        self.second_window.show()

    def edit_test(self):
        """Открывает окно выбора теста для редактирования."""
        self.second_window = ChoiceTestWindow(ChoiceTestWindow.EDIT)
        self.second_window.show()

    def view_statistics(self):
        """Открывает окно выбора теста для просмотра статитстики."""

        self.second_window = ChoiceTestWindow(ChoiceTestWindow.VIEW_STATISTICS)
        self.second_window.show()

    def import_test(self):
        """Импортирует тест из файла CSV."""

        filename = QFileDialog.getOpenFileName(self, 'Выберите файл')[0]
        if filename.split('.')[-1] == 'csv':
            db.import_test(filename)
            self.statusBar().showMessage('Тест доступен для прохождения')
        else:
            self.statusBar().showMessage('Неверный формат файла')

    def export_test(self):
        """Открывает окно для экспорта теста."""

        self.second_window = ChoiceTestWindow(ChoiceTestWindow.EXPORT)
        self.second_window.show()



# Создание окна для создания теста
class CreateWindow(QMainWindow):
    """Класс окна для создания нового теста"""

    def __init__(self, test_id=None):
        """
        Инициализация окна для создания теста.
        Если test_id не None, то окно используется для редактирования существующего теста.
        """

        super().__init__()

        # Загрузка интерфейса из файла
        uic.loadUi('uis/create.ui', self)
        self.setWindowTitle('Создание теста')
        self.initUI()

        # Проверка, является ли окно окном для редактирования теста
        self.update = test_id is not None
        self.test_id = test_id
        self.qs = [] if not self.update else db.get_qas(test_id)

        # Установка количества строк в таблице и заполнение (если тест редактируется)
        self.table.setRowCount(len(self.qs))
        for i in range(len(self.qs)):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.qs[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.qs[i][1])))

    def initUI(self):
        """Инициализация пользовательского интерфейса."""

        self.add_btn.clicked.connect(self.add_question)
        self.finish_btn.clicked.connect(self.finish)
        self.edit_btn.clicked.connect(self.edit)
        self.table.setHorizontalHeaderLabels(['Вопрос', 'Правильный ответ'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.error = QErrorMessage()

    def add_question(self):
        """Добавляет новый вопрос и ответ в таблицу."""
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

    def edit(self):
        """Редактирует выбранный вопрос и ответ."""

        i, ok_pressed = QInputDialog.getText(self, 'Изменение вопроса', 'Введите номер вопроса')
        if not ok_pressed or not i.isdigit() or int(i) - 1 >= len(self.qs) or int(i) - 1 < 0:
            return
        i = int(i) - 1

        q, ok_pressed = QInputDialog.getText(
            self, 'Изменение вопроса', 'Введите новый вопрос (оставьте пустым, чтобы сохранить текущий)'
        )
        if not ok_pressed:
            return

        a, ok_pressed = QInputDialog.getText(
            self, 'Изменение вопроса', f'Введите новый ответ (оставьте пустым, чтобы сохранить текущий)'
        )
        if not ok_pressed:
            return

        old = self.qs[i]
        self.qs[i] = (q if q else old[0], a if a else old[1])
        self.table.setItem(i, 0, QTableWidgetItem(self.qs[i][0]))
        self.table.setItem(i, 1, QTableWidgetItem(self.qs[i][1]))

    def finish(self):
        """Завершает создание теста и сохраняет его в базе данных."""
        if self.name.text().strip() and self.qs and not self.update:
            db.create_test(self.name.text(), self.qs)
            self.close()
            return
        elif self.qs and self.update:
            db.edit_test(
                self.test_id,
                self.name.text().strip() if self.name.text().strip() else db.get_test_name(self.test_id),
                self.qs
            )
            self.close()
            return
        elif not self.name.text().strip():
            self.error.showMessage('Название теста не может быть пустым')
        elif not self.qs:
            self.error.showMessage('Тест должен содержать хотя бы один вопрос')



# Окно выбора теста
class ChoiceTestWindow(QMainWindow):
    """
    Окно для выбора теста. Позволяет выбрать тест для прохождения, просмотра статистики, экспорта результатов или редактирования.
    """

    DO_TEST = 0
    VIEW_STATISTICS = 1
    EXPORT = 2
    EDIT = 3

    def __init__(self, action):
        """Инициализация окна."""
        super().__init__()

        self.action = action

        uic.loadUi('uis/choice_test.ui', self)
        self.setWindowTitle('Выбор теста')
        self.initUI()

    def initUI(self):
        """Инициализация пользовательского интерфейса."""

        if self.action == self.DO_TEST:
            # Прохождение - все тесты из БД
            tests = db.get_test_names()

        elif self.action == self.VIEW_STATISTICS:
            # Результаты - только тесты, для которых сохранены результаты
            self.start_btn.setText('Посмотреть результат')

            test_ids = map(lambda x: int(x.rstrip('.csv')), os.listdir('results'))
            tests = list(map(lambda x: (db.get_test_name(x), x), test_ids))
            if not tests:
                self.statusBar().showMessage('Вы не проходили ни одного теста')
                return

        elif self.action == self.EXPORT:
            # Экспорт - все тесты из БД
            tests = db.get_test_names()
            self.start_btn.setText('Экспорт')

        elif self.action == self.EDIT:
            # Редактирование - все тесты из БД
            tests = db.get_test_names()
            self.start_btn.setText('Редактировать')

        if not tests:
            self.statusBar().showMessage('Тестов не найдено')
            return

        self.test_btns = []

        for i, test in enumerate(tests):
            self.test_btns.append(QRadioButton(test[0], self.groupBox))
            self.test_btns[-1].move(25, i * 25 + 25)
            self.test_btns[-1].toggled.connect(self.select_test)

        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_test)

    def select_test(self):
        """Включает кнопку "Начать" при выборе какого-нибудь варианта."""

        self.start_btn.setEnabled(True)

    def start_test(self):
        """Открывает окно теста или результатов теста в зависимости от выбранного действия."""

        test_name = list(filter(lambda x: x.isChecked(), self.test_btns))[0].text()
        test_id = db.get_test_id(test_name)
        if self.action == self.DO_TEST:
            self.second_window = TestWindow(test_id)
            self.second_window.show()
            self.close()
        elif self.action == self.VIEW_STATISTICS:
            self.second_window = ResultWindow(test_id)
            self.second_window.show()
            self.close()
        elif self.action == self.EXPORT:
            name = db.export_test(test_id)
            self.statusBar().showMessage(f'Сохранено в файл "{name}"')
        elif self.action == self.EDIT:
            self.second_window = CreateWindow(test_id)
            self.second_window.show()
            self.close()



# Окно теста
class TestWindow(QMainWindow):
    """Окно для прохождения теста. Позволяет проходить тест и сохранять ответы."""

    def __init__(self, test_id):
        """Инициализация окна."""

        self.test_id = test_id
        self.test_name = db.get_test_name(self.test_id)
        self.qs = db.get_questions(self.test_id)

        self.question_labels = []
        self.question_line_edits = []

        super().__init__()

        uic.loadUi('uis/test.ui', self)
        self.setWindowTitle(f'Тест "{self.test_name}"')
        self.initUI()

    def initUI(self):
        """Инициализация пользовательского интерфейса окна теста."""

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
        """Сохраняет ответы на вопросы, открывает результаты и закрывает окно теста."""

        answers = [x.text() for x in self.question_line_edits]
        filer.save_answers(answers, db, self.test_id)

        self.close()
        self.second_window = ResultWindow()
        self.second_window.show()



class ResultWindow(QMainWindow):

    def __init__(self, test_id=None):
        """Инициализация окна."""

        super().__init__()

        uic.loadUi('uis/result.ui', self)

        self.test_id = test_id

        self.setWindowTitle(f'Результат теста "{db.get_test_name(self.test_id)}"')
        self.setMaximumSize(500, 500)
        self.setMinimumSize(500, 500)

        if self.test_id is None:
            r, a = filer.get_right_all_count()
        else:
            r, a = filer.get_right_all_count(self.test_id)
        make_result_image(r, a)

        self.initUI()

    def initUI(self):
        """Инициализация пользовательского интерфейса окна теста."""

        self.pixmap = QPixmap('sources/result.png')
        self.img_lbl.setPixmap(self.pixmap)

        self.exit_btn.clicked.connect(self.close)


def make_result_image(right_count, all_count):
    """
    Создание изображения с результатом теста.
    :param right_count: количество правильных ответов
    :param all_count: общее количество вопросов
    """
    
    img = Image.new('RGBA', (500, 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('sources/Roboto.ttf', 40)

    draw.text((275, 220), f'{right_count}/{all_count}', font=myFont, fill=(0, 0, 0, 255))

    draw.rounded_rectangle((125, 150, 250, 350), fill=(220, 220, 220, 255), radius=15)

    p = 1 - right_count / all_count
    if p != 1:
        draw.rounded_rectangle((125, 150 + 200 * p, 250, 350), fill=(0, 200, 0, 255), radius=15)

    img.save('sources/result.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
