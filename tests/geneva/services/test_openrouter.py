import json

import pytest

from geneva.services.openrouter import OpenRouterService


@pytest.fixture
def api_key():
    return "test-api-key"


@pytest.fixture
def service(api_key):
    return OpenRouterService(api_key=api_key)


class TestOpenRouterService:
    def test_initialization(self, service):
        assert service.model_name == "google/gemini-2.0-flash-001"
        assert service.base_url is not None
        assert "Authorization" in service.headers
        assert "Content-Type" in service.headers

    def test_summarize_gene_disease_with_valid_json(
        self, service, monkeypatch
    ):
        sample_data = {
            "gene": "TP53",
            "disease": "Cancer",
            "association_data": {"score": 0.95},
        }
        expected_output = {
            "summary_text": "TP53 is strongly associated with Cancer.",
            "key_findings": ["TP53 mutation linked to Cancer"],
            "confidence": 0.95,
        }

        def mock_ask_model(prompt):
            return json.dumps(expected_output)

        monkeypatch.setattr(service, "_ask_model", mock_ask_model)

        result = service.summarize_gene_disease(sample_data)
        assert result == expected_output

    def test_summarize_gene_disease_with_invalid_json(
        self, service, monkeypatch
    ):
        sample_data = {
            "gene": "BRCA1",
            "disease": "Breast Cancer",
            "association_data": {},
        }

        def mock_ask_model(prompt):
            return "Oops, malformed response"

        monkeypatch.setattr(service, "_ask_model", mock_ask_model)

        result = service.summarize_gene_disease(sample_data)
        assert "Oops, malformed response" in result["summary_text"]
        assert result["key_findings"] == []
        assert result["confidence"] is None

    def test_summarize_gene_disease_with_additional_context(
        self, service, monkeypatch
    ):
        sample_data = {"gene": "EGFR", "disease": "Lung Cancer"}
        additional_context = "Consider latest research papers."

        def mock_ask_model(prompt):
            assert "Consider latest research papers." in prompt
            return json.dumps(
                {
                    "summary_text": "EGFR associated with Lung Cancer.",
                    "key_findings": [
                        "EGFR mutation drives cancer progression"
                    ],
                    "confidence": 0.9,
                }
            )

        monkeypatch.setattr(service, "_ask_model", mock_ask_model)

        result = service.summarize_gene_disease(
            sample_data, additional_context
        )
        assert result["summary_text"] == "EGFR associated with Lung Cancer."
        assert result["key_findings"] == [
            "EGFR mutation drives cancer progression"
        ]
        assert result["confidence"] == 0.9
