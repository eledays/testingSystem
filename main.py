from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QHeaderView, QErrorMessage
from PyQt6 import uic

from databaser import Databaser

import sys


db = Databaser()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)

        self.setWindowTitle('Тестовая система')

        self.initUI()

    def initUI(self):
        self.create_btn.clicked.connect(self.create_test)
        self.edit_btn.clicked.connect(self.edit_test)
        self.do_btn.clicked.connect(self.do_test)
        self.stat_btn.clicked.connect(self.view_statistics)
        self.import_btn.clicked.connect(self.import_test)
        self.export_btn.clicked.connect(self.export_test)

    def do_test(self):
        print('Прохождение теста')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
