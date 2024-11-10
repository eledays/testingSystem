from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Тестовая система')
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.create_btn = QPushButton('Создать тест')
        self.create_btn.clicked.connect(self.create_test)

        self.edit_btn = QPushButton('Редактировать тест')
        self.edit_btn.clicked.connect(self.edit_test)

        self.do_btn = QPushButton('Пройти тест')
        self.do_btn.clicked.connect(self.take_test)

        self.stat_btn = QPushButton('Просмотр статистики')
        self.stat_btn.clicked.connect(self.view_statistics)

        self.import_btn = QPushButton('Импорт тестов')
        self.import_btn.clicked.connect(self.import_test)

        self.export_btn = QPushButton('Экспорт тестов')
        self.export_btn.clicked.connect(self.export_test)

        layout.addWidget(self.create_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.do_btn)
        layout.addWidget(self.stat_btn)
        layout.addWidget(self.import_btn)
        layout.addWidget(self.export_btn)

        central_widget.setLayout(layout)

    def create_test(self):
        print('Создание теста')

    def edit_test(self):
        print('Редактирование теста')

    def take_test(self):
        print('Прохождение теста')

    def view_statistics(self):
        print('Просмотр статистики')

    def import_test(self):
        print('Импорт тестов')

    def export_test(self):
        print('Экспорт тестов')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
