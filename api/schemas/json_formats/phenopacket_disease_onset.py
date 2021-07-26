from api.schemas.json_formats.ontology import OntologyInputType
from api.schemas.json_formats.age_or_age_range import AgeInputType
import strawberry

@strawberry.input
class PhenopacketDiseaseOnsetInputType:
    age: AgeInputType
    ontology: OntologyInputType