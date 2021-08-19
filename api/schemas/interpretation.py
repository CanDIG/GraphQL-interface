
from api.schemas.utils import generic_filter, set_extra_properties
from api.schemas.scalars.json_scalar import JSONScalar
from typing import List, Optional
from api.interfaces.input import Input
import strawberry

@strawberry.input
class InterpretationInputType((Input)):
    id: Optional[strawberry.ID] = None
    resolution_status: Optional[str] = None
    phenopacket: Optional[str] = None
    diagnosis: Optional[str] = None
    meta_data: Optional[str] = None

@strawberry.type
class Interpretation:
    id: Optional[strawberry.ID] = None
    resolution_status: Optional[str] = None
    phenopacket: Optional[str] = None
    diagnosis: Optional[List[str]] = None
    meta_data: Optional[str] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = Interpretation(**json)
        
        set_extra_properties(json, ret)

        return ret

    @staticmethod
    def filter(instance, input: InterpretationInputType):
        return generic_filter(instance, input)