import pytest

from geneva.model import (
    SQLModel,
    create_user,
    engine,
    get_user_by_name,
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
