from api.interfaces.input import Input
from typing import Optional
from api.schemas.json_formats.ontology import OntologyInputType
from api.schemas.json_formats.age_or_age_range import AgeInputType
import strawberry

@strawberry.input
class PhenopacketDiseaseOnsetInputType(Input):
    age: Optional[AgeInputType] = None
    ontology: Optional[OntologyInputType] = None