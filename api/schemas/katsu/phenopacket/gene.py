from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties
from api.schemas.scalars.json_scalar import JSONScalar
from typing import List, Optional
import strawberry


@strawberry.input
class GeneInputType(Input):
    id: Optional[strawberry.ID] = None
    symbol: Optional[str] = None
    
@strawberry.type
class Gene:
    id: Optional[strawberry.ID] = None
    alternate_ids: Optional[List[strawberry.ID]] = None
    symbol: Optional[str] = None
    created: Optional[str] = None
    updated: Optional[str] = None
    extra_properties: Optional[JSONScalar] = None

    @staticmethod
    def deserialize(json):
        ret = Gene(**json)
        
        set_extra_properties(json, ret)
        
        return ret

    @staticmethod
    def filter(instance, input: GeneInputType):
        return generic_filter(instance, input)