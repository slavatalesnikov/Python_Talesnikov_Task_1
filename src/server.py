"""Сервер RPC на основе протокола TCP."""

import socket
import struct
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import models

PROTOCOL_VERSION = 1
HEADER_SIZE = 6
RESET_OP_CODE = 99

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


def recv_all(conn, size):
    """Получить ровно size байт из сокета."""
    data = b""
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data


def parse_header(header):
    """Разобрать заголовок запроса и вернуть version, op_code, body_size."""
    version = header[0]
    op_code = struct.unpack_from("<H", header, 1)[0]
    body_size = struct.unpack_from("<I", header[3:6] + b"\x00")[0]
    return version, op_code, body_size


def call_operation(op_name, body):
    """Вызвать нужную функцию модели по имени операции."""
    if op_name == "entity_create":
        return models.entity_create(
            body["created"], body["ip"],
            body["locale"], body["platform"]
        )
    if op_name == "entity_delete":
        models.entity_delete(body["identifier"])
        return "ok"
    if op_name == "entity_get_all":
        return models.entity_get_all()
    if op_name == "entity_get_by_id":
        return models.entity_get_by_id(body["identifier"])
    if op_name == "assignment_create":
        return models.assignment_create(
            body["created"], body["parameter"], body["entity"],
            body["tags"], body["stage"], body["triggered"]
        )
    if op_name == "assignment_delete":
        models.assignment_delete(body["identifier"])
        return "ok"
    if op_name == "assignment_get_all":
        return models.assignment_get_all()
    if op_name == "assignment_get_by_id":
        return models.assignment_get_by_id(body["identifier"])
    if op_name == "feedback_create":
        return models.feedback_create(
            body["created"], body["output"], body["stage"],
            body["exception"], body["assignment"],
            body["cache_hit"], body["duration"]
        )
    if op_name == "feedback_delete":
        models.feedback_delete(body["identifier"])
        return "ok"
    if op_name == "feedback_get_all":
        return models.feedback_get_all()
    if op_name == "feedback_get_by_id":
        return models.feedback_get_by_id(body["identifier"])
    if op_name == "get_recent_assignments_with_feedback":
        return models.get_recent_assignments_with_feedback()
    return "unknown operation"


def reset_data():
    """Сбросить все данные в моделях (используется в тестах)."""
    models.entities.clear()
    models.assignments.clear()
    models.feedbacks.clear()
    models.entity_next_id = 1
    models.assignment_next_id = 1
    models.feedback_next_id = 1


def build_response(op_code, result):
    """Собрать байты ответа из кода операции и результата."""
    response_body = json.dumps(result).encode("utf-8")
    response_size = struct.pack("<I", len(response_body))
    return bytes([op_code]) + response_size + response_body


def handle_request(conn):
    """Прочитать запрос, выполнить операцию и вернуть ответ."""
    header = recv_all(conn, HEADER_SIZE)
    if len(header) < HEADER_SIZE:
        return None

    version, op_code, body_size = parse_header(header)
    body_bytes = recv_all(conn, body_size) if body_size > 0 else b""
    body = json.loads(body_bytes.decode("utf-8")) if body_size > 0 else {}

    print(f"[LOG] version={version} op_code={op_code} body={body}")

    if op_code == RESET_OP_CODE:
        reset_data()
        return build_response(op_code, "ok")

    op_name = OPERATIONS.get(op_code)
    result = call_operation(op_name, body)
    return build_response(op_code, result)


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
        response = handle_request(conn)
        if response:
            conn.send(response)
        conn.close()


if __name__ == "__main__":
    start_server()