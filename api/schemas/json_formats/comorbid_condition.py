from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_field
from typing import Optional
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
import strawberry

@strawberry.input
class ComorbidConditionInputType(Input):
    clinical_status: Optional[OntologyInputType] = None
    code: Optional[OntologyInputType] = None

@strawberry.type
class ComorbidCondition:
    clinical_status: Optional[Ontology] = None
    code: Optional[Ontology] = None

    @staticmethod
    def deserialize(json):
        ret = ComorbidCondition(**json)
        set_field(json, ret, "clinical_status", Ontology)
        set_field(json, ret, "code", Ontology)
        return 

    @staticmethod
    def filter(instance, input: ComorbidConditionInputType):
        return generic_filter(instance, input)