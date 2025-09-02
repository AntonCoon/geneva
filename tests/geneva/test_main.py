import pytest
from fastapi.testclient import TestClient

from geneva.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    from geneva.model import SQLModel, engine

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "GenEvA is running!"


class TestAuth:
    def test_register_new_user(self):
        response = client.post(
            "/login", json={"username": "alice", "api_key": "key123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["username"] == "alice"

    def test_register_existing_user_fails(self):
        client.post("/login", json={"username": "bob", "api_key": "key123"})
        response = client.post(
            "/login", json={"username": "bob", "api_key": "key999"}
        )
        assert response.status_code == 409
        assert response.json()["status"] == "error"

    def test_login_existing_user_without_api_key(self):
        client.post("/login", json={"username": "carol", "api_key": "key123"})
        response = client.post("/login", json={"username": "carol"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["data"]["username"] == "carol"

    def test_login_nonexistent_user_without_api_key(self):
        response = client.post("/login", json={"username": "dave"})
        assert response.status_code == 404
        assert response.json()["status"] == "error"

    def test_get_user_info_success(self):
        client.post("/login", json={"username": "eve", "api_key": "key123"})
        response = client.get("/user/eve")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["username"] == "eve"
        assert data["has_api_key"] is True

    def test_get_user_info_not_found(self):
        response = client.get("/user/not_exists")
        assert response.status_code == 404
        assert response.json()["status"] == "error"


class TestQueries:
    def test_run_query_and_store_result(self, monkeypatch):
        client.post("/login", json={"username": "alice", "api_key": "key123"})

        def fake_fetch_association(self, gene, disease):
            return {"summary": f"{gene}-{disease}-association"}

        monkeypatch.setattr(
            "geneva.main.OpenTargetService.fetch_association",
            fake_fetch_association,
        )

        response = client.post(
            "/query",
            json={"username": "alice", "gene": "BRCA1", "disease": "cancer"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        data = body["data"]
        assert data["gene"] == "BRCA1"
        assert data["disease"] == "cancer"
        assert data["response"]["summary"] == "BRCA1-cancer-association"

    def test_run_query_for_nonexistent_user(self):
        response = client.post(
            "/query",
            json={"username": "ghost", "gene": "TP53", "disease": "cancer"},
        )
        assert response.status_code == 404
        body = response.json()
        assert body["status"] == "error"

    def test_list_user_queries(self, monkeypatch):
        client.post("/login", json={"username": "bob", "api_key": "key123"})

        def fake_fetch_association(self, gene, disease):
            return {"summary": f"{gene}-{disease}-association"}

        monkeypatch.setattr(
            "geneva.main.OpenTargetService.fetch_association",
            fake_fetch_association,
        )

        client.post(
            "/query",
            json={"username": "bob", "gene": "BRCA1", "disease": "cancer"},
        )
        client.post(
            "/query",
            json={"username": "bob", "gene": "TP53", "disease": "leukemia"},
        )

        response = client.get("/queries/bob")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        data = body["data"]
        assert isinstance(data, list)
        assert len(data) == 2
        genes = {q["gene"] for q in data}
        assert genes == {"BRCA1", "TP53"}

    def test_list_queries_for_nonexistent_user(self):
        response = client.get("/queries/nope")
        assert response.status_code == 404
        body = response.json()
        assert body["status"] == "error"
