from api.schemas.scalars.json_scalar import JSONScalar
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.json_formats.allele import Allele, AlleleInputObject

@strawberry.input
class VariantInputType:
    id: id
    allele_type: str
    allele: AlleleInputObject
    zygosity: OntologyInputType

@strawberry.type
class Variant:
    id: id
    allele_type: str
    allele: Allele
    zygosity: Ontology
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def allele(self, info) -> Allele:
        return self.allele

    @strawberry.field
    def zygosity(self, info) -> Ontology:
        return self.zygosity

    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties