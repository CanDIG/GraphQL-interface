import strawberry
from .ontology import Ontology, OntologyInputType

@strawberry.input
class PhenopacketEvidenceInputType:
    evidence_code: OntologyInputType

@strawberry.type
class PhenopacketEvidence:
    evidence_code: Ontology