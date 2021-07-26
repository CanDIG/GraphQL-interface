from api.schemas.scalars.json_scalar import JSONScalar
from typing import List, Union
import strawberry
from api.schemas.json_formats.age_or_age_range import Age, AgeRange
from api.schemas.json_formats.phenopacket_disease_onset import PhenopacketDiseaseOnsetInputType
from api.schemas.json_formats.ontology import Ontology, OntologyInputType

@strawberry.input
class DiseaseInputType:
    id: id
    term: OntologyInputType
    onset: PhenopacketDiseaseOnsetInputType
    disease_stage: OntologyInputType
    tnm_finding: OntologyInputType

@strawberry.type
class Disease:
    id: id
    term: Ontology
    onset: Union[Age, AgeRange, Ontology]
    disease_stage: Ontology
    tnm_finding: List(Ontology)
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties