from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties
from typing import Optional
from api.schemas.scalars.json_scalar import JSONScalar
import strawberry

@strawberry.input
class ResourceInputType(Input):
    id: Optional[strawberry.ID] = None
    name: Optional[str] = None
    namespace_prefix: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None
    iri_prefix: Optional[str] = None

@strawberry.type
class Resource:
    id: strawberry.ID
    name: str
    namespace_prefix: str
    url: str
    version: str
    iri_prefix: str
    extra_properties: JSONScalar
    created: str
    updated: str

    @staticmethod
    def deserialize(json):
        ret = Resource(**json)

        set_extra_properties(json, ret)
        
        return ret

    @staticmethod
    def filter(instance, input: ResourceInputType):
        return generic_filter(instance, input)