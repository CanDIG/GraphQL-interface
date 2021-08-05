
from api.schemas.utils import generic_filter
from typing import Optional
import strawberry


@strawberry.input
class PhenopacketExternalReferenceInputType:
    id: Optional[str] = None
    description: Optional[str] = None

@strawberry.type
class PhenopacketExternalReference:
    id: str
    description: str

    @staticmethod
    def deserialize(json):
        return PhenopacketExternalReference(**json)

    @staticmethod
    def filter(instance, input: PhenopacketExternalReferenceInputType):
        return generic_filter(instance, input)