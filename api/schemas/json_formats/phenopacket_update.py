
from api.schemas.utils import generic_filter
from typing import Optional
import strawberry


@strawberry.input
class PhenopacketUpdateInputType:
    timestamp: Optional[str] = None
    updated_by: Optional[str] = None
    comment: Optional[str] = None

@strawberry.type
class PhenopacketUpdate:
    timestamp: Optional[str] = None
    updated_by: Optional[str] = None
    comment: Optional[str] = None

    @staticmethod
    def deserialize(json):
        return PhenopacketUpdate(**json)

    @staticmethod
    def filter(instance, input: PhenopacketUpdateInputType):
        return generic_filter(instance, input)