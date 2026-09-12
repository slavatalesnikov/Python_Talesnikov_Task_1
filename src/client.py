"""Клиент RPC — отправляет запросы к серверу по TCP."""

import socket
import struct
import json
import time

HOST = "127.0.0.1"
PORT = 9000
PROTOCOL_VERSION = 1


def send_request(op_code, body=None):
    """Отправить запрос на сервер и получить ответ."""
    body_bytes = json.dumps(body).encode("utf-8") if body else b""
    body_size = len(body_bytes)

    # Структура запроса: 1 байт версия, 2 байта код операции, 3 байта размер тела, тело
    size_bytes = struct.pack("<I", body_size)[:3]
    request = bytes([PROTOCOL_VERSION]) + struct.pack("<H", op_code) + size_bytes + body_bytes

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(request)
        response = s.recv(4096)

    # Читаем ответ: 1 байт код, 4 байта размер, тело
    resp_size = struct.unpack_from("<I", response, 1)[0]
    resp_body = response[5:5 + resp_size]
    return json.loads(resp_body.decode("utf-8"))


# ===== Методы клиента =====

def entity_create(created, ip, locale, platform):
    """Создать Entity на сервере."""
    return send_request(1, {"created": created, "ip": ip, "locale": locale, "platform": platform})

def entity_delete(identifier):
    """Удалить Entity на сервере."""
    return send_request(2, {"identifier": identifier})

def entity_get_all():
    """Получить все Entity с сервера."""
    return send_request(3)

def entity_get_by_id(identifier):
    """Получить Entity по ID с сервера."""
    return send_request(4, {"identifier": identifier})

def assignment_create(created, parameter, entity, tags, stage, triggered):
    """Создать Assignment на сервере."""
    return send_request(5, {"created": created, "parameter": parameter, "entity": entity, "tags": tags, "stage": stage, "triggered": triggered})

def assignment_delete(identifier):
    """Удалить Assignment на сервере."""
    return send_request(6, {"identifier": identifier})

def assignment_get_all():
    """Получить все Assignment с сервера."""
    return send_request(7)

def assignment_get_by_id(identifier):
    """Получить Assignment по ID с сервера."""
    return send_request(8, {"identifier": identifier})

def feedback_create(created, output, stage, exception, assignment, cache_hit, duration):
    """Создать Feedback на сервере."""
    return send_request(9, {"created": created, "output": output, "stage": stage, "exception": exception, "assignment": assignment, "cache_hit": cache_hit, "duration": duration})

def feedback_delete(identifier):
    """Удалить Feedback на сервере."""
    return send_request(10, {"identifier": identifier})

def feedback_get_all():
    """Получить все Feedback с сервера."""
    return send_request(11)

def feedback_get_by_id(identifier):
    """Получить Feedback по ID с сервера."""
    return send_request(12, {"identifier": identifier})

def get_recent_assignments_with_feedback():
    """Получить JOIN запрос с сервера."""
    return send_request(13)


# ===== Демонстрация работы =====

if __name__ == "__main__":
    print("=== Демонстрация RPC клиента ===")
    now = int(time.time())

    print("\n-- Entity --")
    print("Создать:", entity_create(now, "192.168.1.1", "ru", "linux"))
    print("Все:", entity_get_all())
    print("По ID:", entity_get_by_id(1))

    print("\n-- Assignment --")
    print("Создать:", assignment_create(now, "param1", 1, "tag1", "init", 0))
    print("Все:", assignment_get_all())
    print("По ID:", assignment_get_by_id(1))

    print("\n-- Feedback --")
    print("Создать:", feedback_create(now, "ok", "done", "none", 1, 0, 100))
    print("Все:", feedback_get_all())
    print("По ID:", feedback_get_by_id(1))

    print("\n-- JOIN --")
    print("Результат:", get_recent_assignments_with_feedback())

    print("\n-- Удаление --")
    print("Удалить Entity 1:", entity_delete(1))
    print("Entity после удаления:", entity_get_all())