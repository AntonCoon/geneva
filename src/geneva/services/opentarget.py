import httpx

from geneva.services.base import GeneDiseaseService
from geneva.services.opentarget_config import BASE_URL, QUERIES


class OpenTargetService(GeneDiseaseService):

    def _run_query(self, query: str, variables: dict) -> dict:
        with httpx.Client() as client:
            response = client.post(
                BASE_URL, json={"query": query, "variables": variables}
            )
            response.raise_for_status()
            return response.json()

    def _resolve_gene_id(self, gene_name: str) -> str:
        hits = self._run_query(QUERIES.gene, {"queryString": gene_name})[
            "data"
        ]["search"]["hits"]
        if not hits:
            raise ValueError(f"No gene found for {gene_name}")
        return hits[0]["id"]

    def _resolve_disease_id(self, disease_name: str) -> str:
        hits = self._run_query(QUERIES.disease, {"queryString": disease_name})[
            "data"
        ]["search"]["hits"]
        if not hits:
            raise ValueError(f"No disease found for {disease_name}")
        return hits[0]["id"]

    def fetch_association(self, gene_name: str, disease_name: str) -> dict:
        gene_id = self._resolve_gene_id(gene_name)
        disease_id = self._resolve_disease_id(disease_name)
        return self._run_query(
            QUERIES.target_disease,
            {"geneId": gene_id, "diseaseId": disease_id},
        )["data"]["disease"]
