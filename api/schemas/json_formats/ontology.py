from api.interfaces.input import Input
from api.schemas.utils import generic_filter
from typing import Optional
import strawberry

@strawberry.input
class OntologyInputType(Input):
    id: Optional[str] = None
    label: Optional[str] = None

@strawberry.type
class Ontology:
    id: str
    label: str

    @staticmethod
    def deserialize(json):
        return Ontology(**json)
    
    @staticmethod
    def filter(instance, input: OntologyInputType):
        return generic_filter(instance, input)

@strawberry.input
class SampleTissueInputType:
    reference: Optional[str] = None
    display: Optional[str] = None

@strawberry.type
class SampleTissue:
    reference: str
    display: str
    
    @staticmethod
    def deserialize(json):
        return SampleTissue(**json)

    @staticmethod
    def filter(instance, input: SampleTissueInputType):
        return generic_filter(instance, input)