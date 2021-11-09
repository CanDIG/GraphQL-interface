from api.schemas.utils import generic_filter, set_field
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from typing import Optional
import strawberry

@strawberry.input
class ComplexOntologyInputType:
    data_value: Optional[OntologyInputType] = None
    staging_system: Optional[OntologyInputType] = None 


@strawberry.type
class ComplexOntology:
    data_value: Optional[Ontology] = None
    staging_system: Optional[Ontology] = None

    @staticmethod
    def deserialize(json):
        ret = ComplexOntology(**json)
        set_field(json, ret, "data_value", Ontology)
        set_field(json, ret, "staging_system", Ontology)
        return ret

    @staticmethod
    def filter(instance, input: ComplexOntologyInputType):
        return generic_filter(instance, input)