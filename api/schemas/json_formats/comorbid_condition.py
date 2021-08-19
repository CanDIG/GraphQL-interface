from api.interfaces.input import Input
from api.schemas.utils import generic_filter
from typing import Optional
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
import strawberry

@strawberry.input
class ComorbidConditionInputType(Input):
    first_typeof: Optional[OntologyInputType] = None
    second_typeof_id: Optional[OntologyInputType] = None
    second_typeof_label: Optional[str] = None
    first_property: Optional[str] = None
    schema_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

@strawberry.type
class ComorbidCondition:
    first_typeof: Optional[Ontology] = None
    second_typeof: Optional[Ontology] = None
    first_property: Optional[str] = None
    second_property: Optional[str] = None
    schema_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    @staticmethod
    def deserialize(json):
        return ComorbidCondition(**json)

    @staticmethod
    def filter(instance, input: ComorbidConditionInputType):
        return generic_filter(instance, input)