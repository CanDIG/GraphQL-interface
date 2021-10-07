from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field
from typing import Optional
from api.schemas.scalars.json_scalar import JSONScalar
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.json_formats.allele import Allele, AlleleInputType

@strawberry.input
class VariantInputType(Input):
    id: Optional[strawberry.ID] = None
    allele_type: Optional[str] = None
    allele: Optional[AlleleInputType] = None
    zygosity: Optional[OntologyInputType] = None

@strawberry.type
class Variant:
    id: Optional[str] = None
    allele_type: Optional[str] = None
    allele: Optional[Allele] = None
    zygosity: Optional[Ontology] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None
    hgvs_allele: Optional[JSONScalar] = None

    @staticmethod
    def deserialize(json):
        ret = Variant(**json)

        for (field_name, type) in [("allele", Allele), ("zygosity", Ontology)]:
            set_field(json, ret, field_name, type)

        set_extra_properties(json, ret)

        return ret

    @staticmethod
    def filter(instance, input: VariantInputType):
        return generic_filter(instance, input)