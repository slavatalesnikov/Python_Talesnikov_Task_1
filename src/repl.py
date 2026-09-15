"""REPL интерактивный режим для работы с моделью данных."""

import time
import models


def print_help():
    """Вывести список доступных команд."""
    print("""
Доступные команды:

  Entity:
    entity_create       - создать запись Entity
    entity_delete       - удалить запись Entity по ID
    entity_get_all      - показать все записи Entity
    entity_get_by_id    - найти запись Entity по ID

  Assignment:
    assignment_create       - создать запись Assignment
    assignment_delete       - удалить запись Assignment по ID
    assignment_get_all      - показать все записи Assignment
    assignment_get_by_id    - найти запись Assignment по ID

  Feedback:
    feedback_create       - создать запись Feedback
    feedback_delete       - удалить запись Feedback по ID
    feedback_get_all      - показать все записи Feedback
    feedback_get_by_id    - найти запись Feedback по ID

  Прочее:
    join    - показать задания с фидбеком за последние 5 минут
    help    - показать это меню
    exit    - выйти
""")


def handle_entity(command):
    """Обработать команды для Entity."""
    if command == "entity_create":
        created = int(time.time())
        ip = input("Введите ip: ")
        locale = input("Введите locale: ")
        platform = input("Введите platform: ")
        record = models.entity_create(created, ip, locale, platform)
        print("Создано:", record)
    elif command == "entity_delete":
        identifier = int(input("Введите ID: "))
        models.entity_delete(identifier)
        print("Удалено.")
    elif command == "entity_get_all":
        records = models.entity_get_all()
        if records:
            for r in records:
                print(r)
        else:
            print("Список пуст.")
    elif command == "entity_get_by_id":
        identifier = int(input("Введите ID: "))
        record = models.entity_get_by_id(identifier)
        print(record if record else "Не найдено.")


def handle_assignment(command):
    """Обработать команды для Assignment."""
    if command == "assignment_create":
        created = int(time.time())
        parameter = input("Введите parameter: ")
        entity = int(input("Введите entity ID: "))
        tags = input("Введите tags: ")
        stage = input("Введите stage: ")
        triggered = int(input("Введите triggered: "))
        record = models.assignment_create(
            created, parameter, entity, tags, stage, triggered
        )
        print("Создано:", record)
    elif command == "assignment_delete":
        identifier = int(input("Введите ID: "))
        models.assignment_delete(identifier)
        print("Удалено.")
    elif command == "assignment_get_all":
        records = models.assignment_get_all()
        if records:
            for r in records:
                print(r)
        else:
            print("Список пуст.")
    elif command == "assignment_get_by_id":
        identifier = int(input("Введите ID: "))
        record = models.assignment_get_by_id(identifier)
        print(record if record else "Не найдено.")


def handle_feedback(command):
    """Обработать команды для Feedback."""
    if command == "feedback_create":
        created = int(time.time())
        output = input("Введите output: ")
        stage = input("Введите stage: ")
        exception = input("Введите exception: ")
        assignment = int(input("Введите assignment ID: "))
        cache_hit = int(input("Введите cache_hit (0 или 1): "))
        duration = int(input("Введите duration: "))
        record = models.feedback_create(
            created, output, stage, exception,
            assignment, cache_hit, duration
        )
        print("Создано:", record)
    elif command == "feedback_delete":
        identifier = int(input("Введите ID: "))
        models.feedback_delete(identifier)
        print("Удалено.")
    elif command == "feedback_get_all":
        records = models.feedback_get_all()
        if records:
            for r in records:
                print(r)
        else:
            print("Список пуст.")
    elif command == "feedback_get_by_id":
        identifier = int(input("Введите ID: "))
        record = models.feedback_get_by_id(identifier)
        print(record if record else "Не найдено.")


def handle_command(command):
    """Обработать введённую команду."""
    if command == "exit":
        return False
    if command == "help":
        print_help()
    elif command.startswith("entity"):
        handle_entity(command)
    elif command.startswith("assignment"):
        handle_assignment(command)
    elif command.startswith("feedback"):
        handle_feedback(command)
    elif command == "join":
        records = models.get_recent_assignments_with_feedback()
        if records:
            for r in records:
                print(r)
        else:
            print("Нет данных за последние 5 минут.")
    else:
        print("Неизвестная команда. Введите help для списка команд.")
    return True


def main():
    """Главный цикл REPL."""
    print("Добро пожаловать! Введите help для списка команд.")
    while True:
        command = input("\n> ").strip()
        if not handle_command(command):
            print("До свидания!")
            break


if __name__ == "__main__":
    main()