# Тестовая система

![Тестовая система](/sources/logo.png)

## Описание
Это приложение для создания, прохождения и редактирования тестов. Оно использует PyQt6 для создания графического интерфейса и sqlite для хранения тестов.

## Установка
1. Установите Python и необходимые зависимости.
```
pip install -r requirements.txt
```
2. Запустите ```main.py``` с помощью Python.

## Использование

### Создание теста
1. На главном экране нажмите "Создать тест".
2. В появившемся окне введите название теста в соответствующее поле.
3. Нажмите "Добавить вопрос".
4. Введите текст вопроса, например, "Какого цвета небо?" и нажмите "OK".
5. Введите правильный ответ на данный вопрос, например, "синее" (регист не учитывается при проверке) и нажмите "OK".
6. Если необходимо исправить вопрос или ответ на него, нажмите "Изменить вопрос" и следуйте инструкциям на экране.
7. После добавления всех вопросов нажмите "Готово", чтобы сохранить тест.

### Прохождение теста
1. На главном экране нажмите "Пройти тест".
2. В появившемся окне выберите нужный тест и нажмите "Начать прохождение".
3. Вводите ответы на вопросы в соответствующие поля (справа от вопроса) без учёта регистра. Вопрос можно пропустить, оставив поле для ответа пустым.
4. После ввода всех ответов нажмите "Завершить тест". Появится окно с результатами.

### Редактирование теста
1. На главном экране нажмите "Редактировать тест".
2. В появившемся окне выберите нужный тест и нажмите "Редактировать".
3. По аналогии с созданием отредактируйте и сохраните тест.

### Просмотр статистики
1. На главном экране нажмите "Статистика".
2. В появившемся окне выберите нужный тест и нажмите "Посмотреть результат".

### Экспорт тестов
1. На главном экране нажмите "Экспорт тестов".
2. В появившемся окне выберите нужный тест и нажмите "Экспорт". В левом нижнем углу окна отобразится название сохранённого файла.

### Импорт тестов
1. На главном экране нажмите "Импорт тестов".
2. В появившемся окне выберите нужный файл и нажмите "Открыть". В левом нижнем углу окна отобразится информация об успешности добавления.