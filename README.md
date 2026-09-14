# Python_Talesnikov_Task_1

Прототип веб-приложения с удалённым вызовом процедур на основе протокола TCP.
Данные хранятся в памяти, сохранение на диск не производится.

## Описание

Приложение реализует модель слоя доступа к данным для трёх сущностей: Entity, Assignment, Feedback.
Структура данных соответствует ER-диаграмме из задания (Вариант №24).

Для каждой сущности реализованы операции: создание записи, удаление по ID, получение всех записей, получение одной записи по ID.
Также реализована выборка с соединением таблиц Assignment и Feedback за последние 5 минут (LEFT JOIN).

## Структура проекта

src/models.py - модель слоя доступа к данным, все функции для работы с таблицами
src/repl.py - интерактивный режим для демонстрации работы модели (Этап 1)
src/server.py - TCP сервер RPC (Этап 2)
src/client.py - клиент RPC (Этап 2)
tests/test_rpc.py - тесты на основе модели hypothesis (Этап 3)

## Этап 1. Модель слоя доступа к данным

Модель данных в памяти для трёх таблиц: Entity, Assignment, Feedback.
Для каждой таблицы реализованы: создание, удаление, получение всех записей, получение по ID.
Также реализован LEFT JOIN запрос по условию из задания.

Запуск:
python3 src/repl.py

Команды REPL:

entity_create       - создать запись Entity
entity_delete       - удалить запись Entity по ID
entity_get_all      - показать все записи Entity
entity_get_by_id    - найти запись Entity по ID

assignment_create   - создать запись Assignment
assignment_delete   - удалить запись Assignment по ID
assignment_get_all  - показать все записи Assignment
assignment_get_by_id - найти запись Assignment по ID

feedback_create     - создать запись Feedback
feedback_delete     - удалить запись Feedback по ID
feedback_get_all    - показать все записи Feedback
feedback_get_by_id  - найти запись Feedback по ID

join   - показать LEFT JOIN Assignment и Feedback за последние 5 минут
help   - показать список команд
exit   - выйти из программы

Пример использования:

> entity_create
Введите ip: 192.168.1.1
Введите locale: ru
Введите platform: linux
Создано: (1, 1788509241, '192.168.1.1', 'ru', 'linux')

> assignment_create
Введите parameter: test_param
Введите entity ID: 1
Введите tags: tag1
Введите stage: init
Введите triggered: 0
Создано: (1, 1788509302, 'test_param', 1, 'tag1', 'init', 0)

> feedback_create
Введите output: ok
Введите stage: done
Введите exception: none
Введите assignment ID: 1
Введите cache_hit (0 или 1): 0
Введите duration: 100
Создано: (1, 1788509329, 'ok', 'done', 'none', 1, 0, 100)

> join
('test_param', 0, 'ok')

## Этап 2. Удалённый вызов процедур на основе TCP

Реализован сервер и клиент RPC на основе протокола TCP.
Клиент отправляет запросы серверу, сервер выполняет функции модели данных и возвращает результат.
Все запросы логируются в стандартный вывод.

Структура запроса:
- байт 0: версия протокола (1 байт)
- байт 1-2: код операции (2 байта)
- байт 3-5: размер тела запроса (3 байта)
- байт 6+: тело в формате JSON

Структура ответа:
- байт 0: код операции (1 байт)
- байт 1-4: размер тела ответа (4 байта)
- байт 5+: тело в формате JSON

Коды операций:
1  - entity_create
2  - entity_delete
3  - entity_get_all
4  - entity_get_by_id
5  - assignment_create
6  - assignment_delete
7  - assignment_get_all
8  - assignment_get_by_id
9  - feedback_create
10 - feedback_delete
11 - feedback_get_all
12 - feedback_get_by_id
13 - get_recent_assignments_with_feedback

Запуск сервера (Терминал 1):
python3 src/server.py

Запуск клиента - демонстрация всех операций (Терминал 2):
python3 src/client.py

## Этап 3. Тестирование на основе модели

Реализовано тестирование RPC на основе модели (Model-Based Testing, MBT) с использованием библиотеки hypothesis.
Тесты находятся в файле tests/test_rpc.py и покрывают все 13 методов RPC.
Hypothesis автоматически генерирует различные входные данные и проверяет корректность работы сервера.
Используется класс RuleBasedStateMachine из библиотеки hypothesis.

Запуск тестов - сервер должен быть запущен в первом терминале:
pytest tests/test_rpc.py -v --cov=src --cov-report=term-missing