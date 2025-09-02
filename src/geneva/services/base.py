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
