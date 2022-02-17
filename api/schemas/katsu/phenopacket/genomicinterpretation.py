
from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field
from typing import Optional
from api.schemas.scalars.json_scalar import JSONScalar
import strawberry
from api.schemas.katsu.phenopacket.gene import Gene, GeneInputType
from api.schemas.katsu.phenopacket.variant import Variant, VariantInputType

@strawberry.input
class GenomicInterpretationInputType(Input):
    id: Optional[strawberry.ID] = None
    status: Optional[str] = None
    gene: Optional[GeneInputType] = None
    variant: Optional[VariantInputType] = None

@strawberry.type
class GenomicInterpretation:
    id: Optional[strawberry.ID] = None
    status: Optional[str] = None
    gene: Optional[Gene] = None
    variant: Optional[Variant] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = GenomicInterpretation(**json)

        set_field(json, ret, "gene", Gene)

        set_field(json, ret, "variant", Variant)

        set_extra_properties(json, ret)

        return ret

    @staticmethod
    def filter(instance, input: GenomicInterpretationInputType):
        return generic_filter(instance, input)