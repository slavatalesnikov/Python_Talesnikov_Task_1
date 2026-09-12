"""Сервер RPC на основе протокола TCP."""

import socket
import struct
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import models

# Версия протокола
PROTOCOL_VERSION = 1

# Коды операций
OPERATIONS = {
    1:  "entity_create",
    2:  "entity_delete",
    3:  "entity_get_all",
    4:  "entity_get_by_id",
    5:  "assignment_create",
    6:  "assignment_delete",
    7:  "assignment_get_all",
    8:  "assignment_get_by_id",
    9:  "feedback_create",
    10: "feedback_delete",
    11: "feedback_get_all",
    12: "feedback_get_by_id",
    13: "get_recent_assignments_with_feedback",
}


def handle_request(data):
    """Обработать входящий запрос и вернуть ответ."""

    # Читаем заголовок запроса
    # 1 байт - версия, 2 байта - код операции, 3 байта - размер тела
    version = data[0]
    op_code = struct.unpack_from("<H", data, 1)[0]
    body_size = struct.unpack_from("<I", data[3:6] + b"\x00")[0]

    # Читаем тело запроса (JSON)
    body_bytes = data[6:6 + body_size]
    body = json.loads(body_bytes.decode("utf-8")) if body_size > 0 else {}

    print(f"[LOG] version={version} op_code={op_code} body={body}")

    # Вызываем нужную функцию
    op_name = OPERATIONS.get(op_code)
    result = None

    if op_name == "entity_create":
        result = models.entity_create(body["created"], body["ip"], body["locale"], body["platform"])
    elif op_name == "entity_delete":
        models.entity_delete(body["identifier"])
        result = "ok"
    elif op_name == "entity_get_all":
        result = models.entity_get_all()
    elif op_name == "entity_get_by_id":
        result = models.entity_get_by_id(body["identifier"])
    elif op_name == "assignment_create":
        result = models.assignment_create(body["created"], body["parameter"], body["entity"], body["tags"], body["stage"], body["triggered"])
    elif op_name == "assignment_delete":
        models.assignment_delete(body["identifier"])
        result = "ok"
    elif op_name == "assignment_get_all":
        result = models.assignment_get_all()
    elif op_name == "assignment_get_by_id":
        result = models.assignment_get_by_id(body["identifier"])
    elif op_name == "feedback_create":
        result = models.feedback_create(body["created"], body["output"], body["stage"], body["exception"], body["assignment"], body["cache_hit"], body["duration"])
    elif op_name == "feedback_delete":
        models.feedback_delete(body["identifier"])
        result = "ok"
    elif op_name == "feedback_get_all":
        result = models.feedback_get_all()
    elif op_name == "feedback_get_by_id":
        result = models.feedback_get_by_id(body["identifier"])
    elif op_name == "get_recent_assignments_with_feedback":
        result = models.get_recent_assignments_with_feedback()
    else:
        result = "unknown operation"

    # Формируем ответ
    response_body = json.dumps(result).encode("utf-8")
    response_size = struct.pack("<I", len(response_body))

    # Структура ответа: 1 байт код операции, 4 байта размер, тело
    response = bytes([op_code]) + response_size + response_body
    return response


def start_server(host="127.0.0.1", port=9000):
    """Запустить TCP сервер."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        conn, addr = server.accept()
        print(f"[LOG] Подключился клиент: {addr}")
        data = conn.recv(4096)
        if data:
            response = handle_request(data)
            conn.send(response)
        conn.close()


if __name__ == "__main__":
    start_server()