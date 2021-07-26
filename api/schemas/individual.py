from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.json_formats.age_or_age_range import Age, AgeRange
from typing import List, Union
import strawberry
from api.schemas.json_formats.comorbid_condition import ComorbidCondition, ComorbidConditionInputType
from api.schemas.json_formats.age_or_age_range import AgeInputType, AgeUnion
from api.schemas.json_formats.ontology import Ontology, OntologyInputType

@strawberry.input
class IndividualInputType:
    id: id
    date_of_birth: str
    sex: str
    taxonomy: OntologyInputType
    active: bool
    comorbid_condition: ComorbidConditionInputType
    ecog_performance_status: OntologyInputType
    karnofsky: OntologyInputType
    race: str
    ethnicity: str

@strawberry.type
class Individual:
    id: id
    alternate_ids: List(id)
    date_of_birth: str
    age: Union[Age, AgeRange]
    sex: str
    karyotypic_sex: str
    taxonomy: Ontology
    active: bool
    deceased: bool
    comorbid_condition: ComorbidCondition
    ecog_performance_status: Ontology
    karnofsky: Ontology
    race: str
    ethnicity: str
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def age(self, info) -> Union[Age, AgeRange]:
        return self.age
    
    @strawberry.field
    def taxonomy(self, info) -> Ontology:
        return self.taxonomy
    
    @strawberry.field
    def comorbid_condition(self, info) -> ComorbidCondition:
        return self.comorbid_condition
    
    @strawberry.field
    def ecog_performance_status(self, info) -> Ontology:
        return self.ecog_performance_status
    
    @strawberry.field
    def karnofsky(self, info) -> Ontology:
        return self.karnofsky
    
    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties

def filter_individual(instance, input):
    return all(item in instance.items() for item in input.items())