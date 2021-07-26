
from api.schemas.scalars.json_scalar import JSONScalar
from typing import List
import strawberry


@strawberry.input
class InterpretationInputType:
    id: id
    resolution_status: str
    phenopacket: str
    diagnosis: str
    meta_data: str

@strawberry.field
class Interpretation:
    id: id
    resolution_status: str
    phenopacket: str
    diagnosis: List(str)
    meta_data: str
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties