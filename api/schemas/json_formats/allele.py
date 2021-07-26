import strawberry

@strawberry.input
class AlleleInputObject:
    id: str
    hgvs: str
    genome_assembly: str
    chr: str
    pos: str
    ref: str
    alt: str
    info: str
    seq_id: str
    position: int
    deleted_sequence: str
    inserted_sequence: str
    iscn: str

@strawberry.type
class Allele:
    id: str
    hgvs: str
    genome_assembly: str
    chr: str
    pos: str
    ref: str
    alt: str
    info: str
    seq_id: str
    position: int
    deleted_sequence: str
    inserted_sequence: str
    iscn: str