from abc import ABC, abstractmethod
from typing import Any, Dict


class GeneDiseaseService(ABC):

    @abstractmethod
    def fetch_association(
        self, gene_name: str, disease_name: str
    ) -> Dict[str, Any]:
        """
        Fetch gene-disease association for the given gene and disease names.
        Must return a JSON-serializable dict with relevant fields.
        """
        pass


class LLMService(ABC):

    @abstractmethod
    def summarize_gene_disease(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Take a gene-disease association dictionary (from GeneDiseaseService)
        and return a JSON-serializable summary with cleaned information.

        Expected output fields (example):
            - summary_text: str
            - key_findings: list[str]
            - confidence: Optional[float]
        """
        pass
