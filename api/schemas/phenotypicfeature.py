from typing import List
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.scalars.json_scalar import JSONScalar

@strawberry.input
class PhenotypicFeatureInputType:
    id: id
    description: str
    type: OntologyInputType
    negated: bool
    severity: OntologyInputType
    modifier: List(OntologyInputType)
    onset: OntologyInputType
    evidence: OntologyInputType
    biosample: str
    phenopacket: str
    

@strawberry.type
class PhenotypicFeature:
    id: id
    description: str
    type: Ontology
    negated: bool
    severity: Ontology
    modifier: List(Ontology)
    onset: Ontology
    evidence: Ontology
    biosample: str
    phenopacket: str
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def type(self, info) -> Ontology:
        return self.type

    @strawberry.field
    def severity(self, info) -> Ontology:
        return self.severity

    @strawberry.field
    def modifier(self, info) -> List(Ontology):
        return self.modifier

    @strawberry.field
    def onset(self, info) -> Ontology:
        return self.onset

    @strawberry.field
    def evidence(self, info) -> Ontology:
        return self.evidence

    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties