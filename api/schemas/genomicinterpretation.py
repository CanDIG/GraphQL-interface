
from api.schemas.scalars.json_scalar import JSONScalar
import strawberry
from api.schemas.gene import Gene, GeneInputType
from api.schemas.variant import Variant, VariantInputType

@strawberry.input
class GenomicInterpretationInputType:
    id: id
    status: str
    gene: GeneInputType
    variant: VariantInputType

@strawberry.type
class GenomicInterpretation:
    id: id
    status: str
    gene: Gene
    variant: Variant
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def gene(self, info):
        return self.gene

    @strawberry.field
    def variant(self, info):
        return self.variant