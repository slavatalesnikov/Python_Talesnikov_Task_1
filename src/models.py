"""Модель слоя доступа к данным. Хранение в памяти."""

# Хранилища данных просто списки кортежей
entities = []
assignments = []
feedbacks = []

# Счётчики для автоматической генерации ID
entity_next_id = 1
assignment_next_id = 1
feedback_next_id = 1


#Entity

def entity_create(created, ip, locale, platform):
    """Создать новую запись Entity."""
    global entity_next_id
    record = (entity_next_id, created, ip, locale, platform)
    entities.append(record)
    entity_next_id += 1
    return record

def entity_delete(identifier):
    """Удалить запись Entity по ID."""
    global entities
    entities = [e for e in entities if e[0] != identifier]

def entity_get_all():
    """Получить все записи Entity."""
    return list(entities)

def entity_get_by_id(identifier):
    """Получить одну запись Entity по ID."""
    for e in entities:
        if e[0] == identifier:
            return e
    return None


#Assignment

def assignment_create(created, parameter, entity, tags, stage, triggered):
    """Создать новую запись Assignment."""
    global assignment_next_id
    record = (assignment_next_id, created, parameter, entity, tags, stage, triggered)
    assignments.append(record)
    assignment_next_id += 1
    return record

def assignment_delete(identifier):
    """Удалить запись Assignment по ID."""
    global assignments
    assignments = [a for a in assignments if a[0] != identifier]

def assignment_get_all():
    """Получить все записи Assignment."""
    return list(assignments)

def assignment_get_by_id(identifier):
    """Получить одну запись Assignment по ID."""
    for a in assignments:
        if a[0] == identifier:
            return a
    return None


#Feedback

def feedback_create(created, output, stage, exception, assignment, cache_hit, duration):
    """Создать новую запись Feedback."""
    global feedback_next_id
    record = (feedback_next_id, created, output, stage, exception, assignment, cache_hit, duration)
    feedbacks.append(record)
    feedback_next_id += 1
    return record

def feedback_delete(identifier):
    """Удалить запись Feedback по ID."""
    global feedbacks
    feedbacks = [f for f in feedbacks if f[0] != identifier]

def feedback_get_all():
    """Получить все записи Feedback."""
    return list(feedbacks)

def feedback_get_by_id(identifier):
    """Получить одну запись Feedback по ID."""
    for f in feedbacks:
        if f[0] == identifier:
            return f
    return None


# JOIN запрос

def get_recent_assignments_with_feedback():
    """
    Выборка: соединение Assignment и Feedback.
    Берём Feedback созданные за последние 5 минут,
    соединяем с Assignment по полю assignment = identifier.
    Возвращаем: parameter, cache_hit, output.
    """
    import time
    now = time.time()
    five_minutes_ago = now - 5 * 60

    result = []
    for f in feedbacks:
        if f[1] > five_minutes_ago:
            for a in assignments:
                if a[0] == f[5]:
                    result.append((a[2], f[6], f[2]))  # parameter, cache_hit, output
    return result