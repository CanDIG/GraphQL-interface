from api.schemas.scalars.json_scalar import JSONScalar
from typing import List
import strawberry
from api.schemas.genomicinterpretation import GenomicInterpretation, GenomicInterpretationInputType
@strawberry.input
class DiagnosisInputType:
    id: id
    disease: str
    genomic_interpretations: GenomicInterpretationInputType

@strawberry.type
class Diagnosis:
    id: id
    disease: str
    genomic_interpretations: List(GenomicInterpretation)
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties