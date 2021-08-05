from api.schemas.utils import generic_filter, set_extra_properties, set_field_list
from api.schemas.scalars.json_scalar import JSONScalar
from typing import List, Optional
import strawberry
from api.schemas.genomicinterpretation import GenomicInterpretation, GenomicInterpretationInputType


@strawberry.input
class DiagnosisInputType:
    id: Optional[strawberry.ID] = None
    disease: Optional[str] = None
    genomic_interpretations: Optional[GenomicInterpretationInputType] = None

@strawberry.type
class Diagnosis:
    id: Optional[strawberry.ID] = None
    disease: Optional[str] = None
    genomic_interpretations: Optional[List[GenomicInterpretation]] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = Diagnosis(**json)
        
        set_field_list(json, ret, "genomic_interpretations", GenomicInterpretation)

        set_extra_properties(json, ret)
        
        return ret

    @staticmethod
    def filter(instance, input: DiagnosisInputType):
        return generic_filter(instance, input)