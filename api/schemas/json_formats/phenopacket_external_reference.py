
import strawberry


@strawberry.input
class PhenopacketExternalReferenceInputType:
    id: str
    description: str

@strawberry.type
class PhenopacketExternalReference:
    id: str
    description: str