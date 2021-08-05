from api.schemas.utils import generic_filter
from typing import Optional
import strawberry

@strawberry.input
class AlleleInputType:
    id: Optional[strawberry.ID] = None
    hgvs: Optional[str] = None
    genome_assembly: Optional[str] = None
    chr: Optional[str] = None
    pos: Optional[str] = None
    ref: Optional[str] = None
    alt: Optional[str] = None
    info: Optional[str] = None
    seq_id: Optional[str] = None
    position: Optional[int] = None
    deleted_sequence: Optional[str] = None
    inserted_sequence: Optional[str] = None
    iscn: Optional[str] = None

@strawberry.type
class Allele:
    id: Optional[strawberry.ID] = None
    hgvs: Optional[str] = None
    genome_assembly: Optional[str] = None
    chr: Optional[str] = None
    pos: Optional[str] = None
    ref: Optional[str] = None
    alt: Optional[str] = None
    info: Optional[str] = None
    seq_id: Optional[str] = None
    position: Optional[int] = None
    deleted_sequence: Optional[str] = None
    inserted_sequence: Optional[str] = None
    iscn: Optional[str] = None

    @staticmethod
    def deserialize(json):
        return Allele(**json)

    @staticmethod
    def filter(instance, input: AlleleInputType):
        return generic_filter(instance, input)