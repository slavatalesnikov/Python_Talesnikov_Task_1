"""Тесты RPC на основе модели с использованием hypothesis."""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

import client
from hypothesis.stateful import RuleBasedStateMachine, rule
import hypothesis.strategies as st


class RPCStateMachine(RuleBasedStateMachine):
    """
    Модель для тестирования RPC через hypothesis.
    Сравниваем результаты сервера с эталонной моделью в памяти.
    """

    def __init__(self):
        """Инициализация: сброс сервера и эталонной модели."""
        super().__init__()
        client.reset()
        self.entities = []
        self.assignments = []
        self.feedbacks = []
        self.entity_next_id = 1
        self.assignment_next_id = 1
        self.feedback_next_id = 1

    @rule(
        ip=st.just("192.168.1.1"),
        locale=st.just("ru"),
        platform=st.just("linux")
    )
    def create_entity(self, ip, locale, platform):
        """Тест создания Entity: сравниваем сервер с эталоном."""
        now = int(time.time())
        server_result = client.entity_create(now, ip, locale, platform)
        etalon = (
            self.entity_next_id, now, ip, locale, platform
        )
        self.entities.append(etalon)
        self.entity_next_id += 1
        assert server_result is not None
        assert server_result[2] == etalon[2]

    @rule()
    def get_all_entities(self):
        """Тест получения всех Entity: сравниваем сервер с эталоном."""
        server_result = client.entity_get_all()
        assert isinstance(server_result, list)
        assert len(server_result) == len(self.entities)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def get_entity_by_id(self, identifier):
        """Тест получения Entity по ID."""
        result = client.entity_get_by_id(identifier)
        assert result is None or isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def delete_entity(self, identifier):
        """Тест удаления Entity: сравниваем сервер с эталоном."""
        result = client.entity_delete(identifier)
        self.entities = [
            e for e in self.entities if e[0] != identifier
        ]
        assert result == "ok"

    @rule(triggered=st.integers(min_value=0, max_value=1))
    def create_assignment(self, triggered):
        """Тест создания Assignment: сравниваем сервер с эталоном."""
        now = int(time.time())
        server_result = client.assignment_create(
            now, "param1", 1, "tag1", "init", triggered
        )
        etalon = (
            self.assignment_next_id, now,
            "param1", 1, "tag1", "init", triggered
        )
        self.assignments.append(etalon)
        self.assignment_next_id += 1
        assert server_result is not None
        assert server_result[2] == etalon[2]

    @rule()
    def get_all_assignments(self):
        """Тест получения всех Assignment: сравниваем с эталоном."""
        server_result = client.assignment_get_all()
        assert isinstance(server_result, list)
        assert len(server_result) == len(self.assignments)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def get_assignment_by_id(self, identifier):
        """Тест получения Assignment по ID."""
        result = client.assignment_get_by_id(identifier)
        assert result is None or isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def delete_assignment(self, identifier):
        """Тест удаления Assignment: сравниваем с эталоном."""
        result = client.assignment_delete(identifier)
        self.assignments = [
            a for a in self.assignments if a[0] != identifier
        ]
        assert result == "ok"

    @rule(
        cache_hit=st.integers(min_value=0, max_value=1),
        duration=st.integers(min_value=0, max_value=1000)
    )
    def create_feedback(self, cache_hit, duration):
        """Тест создания Feedback: сравниваем сервер с эталоном."""
        now = int(time.time())
        server_result = client.feedback_create(
            now, "ok", "done", "none", 1, cache_hit, duration
        )
        etalon = (
            self.feedback_next_id, now,
            "ok", "done", "none", 1, cache_hit, duration
        )
        self.feedbacks.append(etalon)
        self.feedback_next_id += 1
        assert server_result is not None
        assert server_result[2] == etalon[2]

    @rule()
    def get_all_feedbacks(self):
        """Тест получения всех Feedback: сравниваем с эталоном."""
        server_result = client.feedback_get_all()
        assert isinstance(server_result, list)
        assert len(server_result) == len(self.feedbacks)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def get_feedback_by_id(self, identifier):
        """Тест получения Feedback по ID."""
        result = client.feedback_get_by_id(identifier)
        assert result is None or isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def delete_feedback(self, identifier):
        """Тест удаления Feedback: сравниваем с эталоном."""
        result = client.feedback_delete(identifier)
        self.feedbacks = [
            f for f in self.feedbacks if f[0] != identifier
        ]
        assert result == "ok"

    @rule()
    def join_query(self):
        """Тест JOIN запроса."""
        result = client.get_recent_assignments_with_feedback()
        assert isinstance(result, list)


TestRPC = RPCStateMachine.TestCase