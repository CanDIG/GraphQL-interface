from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field
from typing import Optional
from api.schemas.scalars.json_scalar import JSONScalar
import strawberry
import uuid
from api.schemas.json_formats.ontology import Ontology, OntologyInputType

@strawberry.input
class ProcedureInputType(Input):
    code: Optional[OntologyInputType] = None
    body_site: Optional[OntologyInputType] = None

@strawberry.type
class Procedure:
    code: Ontology
    body_site: Ontology
    extra_properties: JSONScalar
    created: str
    updated: str

    @staticmethod
    def deserialize(json):
        ret = Procedure(**json)
        
        for (field_name, type) in [("code", Ontology), ("body_site", Ontology)]:
            set_field(json, ret, field_name, type)

        set_extra_properties(json, ret)

        return ret

    @staticmethod
    def filter(instance, input: ProcedureInputType):
        return generic_filter(instance, input)