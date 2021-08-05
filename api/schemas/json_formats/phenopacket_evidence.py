from api.schemas.utils import generic_filter
from typing import Optional
import strawberry
from .ontology import Ontology, OntologyInputType

@strawberry.input
class PhenopacketEvidenceInputType:
    evidence_code: Optional[OntologyInputType] = None

@strawberry.type
class PhenopacketEvidence:
    evidence_code: Ontology
    
    @staticmethod
    def deserialize(json):
        return PhenopacketEvidence(**json)
    
    @staticmethod
    def filter(instance, input: PhenopacketEvidenceInputType):
        return generic_filter(instance, input)