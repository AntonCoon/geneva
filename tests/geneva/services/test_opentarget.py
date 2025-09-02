import pytest

from geneva.services.opentarget import OpenTargetService
from geneva.services.opentarget_config import QUERIES

MOCK_GENE_RESPONSE = {"data": {"search": {"hits": [{"id": "ENSG000001"}]}}}
MOCK_DISEASE_RESPONSE = {"data": {"search": {"hits": [{"id": "EFO_0001"}]}}}
MOCK_ASSOCIATION_RESPONSE = {
    "data": {
        "disease": {
            "id": "EFO_0001",
            "name": "Cancer",
            "evidences": {"count": 1, "rows": []},
        }
    }
}


@pytest.fixture
def service():
    return OpenTargetService()


def test_resolve_gene_id(monkeypatch, service):
    monkeypatch.setattr(service, "_run_query", lambda q, v: MOCK_GENE_RESPONSE)
    gene_id = service._resolve_gene_id("TP53")
    assert gene_id == "ENSG000001"


def test_resolve_disease_id(monkeypatch, service):
    monkeypatch.setattr(
        service, "_run_query", lambda q, v: MOCK_DISEASE_RESPONSE
    )
    disease_id = service._resolve_disease_id("Cancer")
    assert disease_id == "EFO_0001"


def test_fetch_association(monkeypatch, service):
    def mock_run_query(query, variables):
        if query == QUERIES.gene:
            return MOCK_GENE_RESPONSE
        elif query == QUERIES.disease:
            return MOCK_DISEASE_RESPONSE
        elif query == QUERIES.target_disease:
            return MOCK_ASSOCIATION_RESPONSE
        raise ValueError("Unexpected query")

    monkeypatch.setattr(service, "_run_query", mock_run_query)

    result = service.fetch_association("TP53", "Cancer")
    assert result["id"] == "EFO_0001"
    assert result["name"] == "Cancer"
    assert "evidences" in result
