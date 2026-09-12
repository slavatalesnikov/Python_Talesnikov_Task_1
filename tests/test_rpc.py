"""Тесты RPC на основе модели (Model-Based Testing) с использованием hypothesis."""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

import client
from hypothesis.stateful import RuleBasedStateMachine, rule
import hypothesis.strategies as st


class RPCStateMachine(RuleBasedStateMachine):
    """Модель для тестирования RPC через hypothesis."""

    def __init__(self):
        super().__init__()
        # Сбрасываем данные на сервере перед каждым тестом
        client.reset()

    @rule(
        ip=st.just("192.168.1.1"),
        locale=st.just("ru"),
        platform=st.just("linux")
    )
    def create_entity(self, ip, locale, platform):
        """Тест создания Entity."""
        now = int(time.time())
        result = client.entity_create(now, ip, locale, platform)
        assert result is not None
        assert result[2] == ip

    @rule()
    def get_all_entities(self):
        """Тест получения всех Entity."""
        result = client.entity_get_all()
        assert isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def get_entity_by_id(self, identifier):
        """Тест получения Entity по ID."""
        result = client.entity_get_by_id(identifier)
        assert result is None or isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def delete_entity(self, identifier):
        """Тест удаления Entity."""
        result = client.entity_delete(identifier)
        assert result == "ok"

    @rule(triggered=st.integers(min_value=0, max_value=1))
    def create_assignment(self, triggered):
        """Тест создания Assignment."""
        now = int(time.time())
        result = client.assignment_create(now, "param1", 1, "tag1", "init", triggered)
        assert result is not None
        assert result[2] == "param1"

    @rule()
    def get_all_assignments(self):
        """Тест получения всех Assignment."""
        result = client.assignment_get_all()
        assert isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def get_assignment_by_id(self, identifier):
        """Тест получения Assignment по ID."""
        result = client.assignment_get_by_id(identifier)
        assert result is None or isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def delete_assignment(self, identifier):
        """Тест удаления Assignment."""
        result = client.assignment_delete(identifier)
        assert result == "ok"

    @rule(
        cache_hit=st.integers(min_value=0, max_value=1),
        duration=st.integers(min_value=0, max_value=1000)
    )
    def create_feedback(self, cache_hit, duration):
        """Тест создания Feedback."""
        now = int(time.time())
        result = client.feedback_create(now, "ok", "done", "none", 1, cache_hit, duration)
        assert result is not None
        assert result[2] == "ok"

    @rule()
    def get_all_feedbacks(self):
        """Тест получения всех Feedback."""
        result = client.feedback_get_all()
        assert isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def get_feedback_by_id(self, identifier):
        """Тест получения Feedback по ID."""
        result = client.feedback_get_by_id(identifier)
        assert result is None or isinstance(result, list)

    @rule(identifier=st.integers(min_value=1, max_value=5))
    def delete_feedback(self, identifier):
        """Тест удаления Feedback."""
        result = client.feedback_delete(identifier)
        assert result == "ok"

    @rule()
    def join_query(self):
        """Тест JOIN запроса."""
        result = client.get_recent_assignments_with_feedback()
        assert isinstance(result, list)


TestRPC = RPCStateMachine.TestCase