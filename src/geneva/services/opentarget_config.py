# flake8: noqa
from dataclasses import dataclass

BASE_URL = "https://api.platform.opentargets.org/api/v4/graphql"


@dataclass(frozen=True)
class Queries:
    gene: str
    disease: str
    target_disease: str


QUERIES = Queries(
    gene="""
    query findTarget($queryString: String!) {
      search(queryString: $queryString, entityNames: ["target"], page: { index: 0, size: 1 }) {
        hits { id }
      }
    }
    """,
    disease="""
    query findDisease($queryString: String!) {
      search(queryString: $queryString, entityNames: ["disease"], page: { index: 0, size: 1 }) {
        hits { id }
      }
    }
    """,
    target_disease="""
    query targetDiseaseEvidence($diseaseId: String!, $geneId: String!) {
      disease(efoId: $diseaseId) {
        id
        name
        evidences(ensemblIds: [$geneId]) {
          count
          rows {
            disease { id name }
            diseaseFromSource
            target { id approvedSymbol }
            mutatedSamples {
              functionalConsequence { id label }
              numberSamplesTested
              numberMutatedSamples
            }
            resourceScore
            significantDriverMethods
            cohortId
            cohortShortName
            cohortDescription
          }
        }
      }
    }
    """,
)
