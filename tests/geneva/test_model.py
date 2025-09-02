import json
from datetime import datetime

import pytest

from geneva.model import (
    SQLModel,
    create_user,
    engine,
    get_user_by_name,
    get_user_queries,
    save_user_query,
    user_exists,
)


@pytest.fixture(autouse=True)
def reset_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield


class TestUserModel:
    def test_create_user(self):
        user = create_user("alice", "key123")
        assert user.id is not None
        assert user.username == "alice"
        assert user.api_key == "key123"

    def test_get_user_by_name(self):
        create_user("bob", "key456")
        user = get_user_by_name("bob")
        assert user is not None
        assert user.username == "bob"
        assert user.api_key == "key456"

    def test_user_exists(self):
        assert not user_exists("carol")
        create_user("carol", "key789")
        assert user_exists("carol")


class TestUserQueryModel:
    def test_save_and_get_user_query_without_llm(self):
        user = create_user("dave", "key001")
        response_data = {"some": "result", "value": 42}
        save_user_query(user.id, "TP53", "cancer", response_data)

        queries = get_user_queries(user.id)
        assert len(queries) == 1
        uq = queries[0]
        assert uq.user_id == user.id
        assert uq.gene == "TP53"
        assert uq.disease == "cancer"
        assert isinstance(uq.service_response, str)
        assert uq.llm_response is None
        loaded = json.loads(uq.service_response)
        assert loaded == response_data

    def test_save_and_get_user_query_with_llm(self):
        user = create_user("frank", "key002")
        service_response = {"score": 0.95}
        llm_response = {
            "summary_text": "TP53 is associated with cancer",
            "key_findings": ["Mutation found in TP53 gene"],
            "confidence": 0.95,
        }

        save_user_query(
            user.id,
            "TP53",
            "cancer",
            service_response,
            llm_response=llm_response,
        )

        queries = get_user_queries(user.id)
        assert len(queries) == 1
        uq = queries[0]
        loaded_service = json.loads(uq.service_response)
        loaded_llm = json.loads(uq.llm_response)
        assert loaded_service == service_response
        assert loaded_llm == llm_response

    def test_timestamp_set(self):
        user = create_user("eve", "key003")
        response_data = {"test": True}
        save_user_query(user.id, "BRCA1", "breast cancer", response_data)

        queries = get_user_queries(user.id)
        uq = queries[0]
        assert isinstance(uq.created_at, datetime)
        assert uq.created_at <= datetime.now()
