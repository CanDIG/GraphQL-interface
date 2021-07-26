from api.schemas.scalars.json_scalar import JSONScalar
from typing import List
import strawberry


@strawberry.input
class GeneInputType:
    id: id
    symbol: str
    
@strawberry.type
class Gene:
    id: id
    alternate_ids: List(str)
    symbol: str
    created: str
    updated: str
    extra_properties: JSONScalar

    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties
