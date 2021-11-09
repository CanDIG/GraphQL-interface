from api.schemas.utils import generic_filter
from typing import Optional
import strawberry

@strawberry.input
class QuantityInputType:
    value: Optional[float] = None
    comparator: Optional[str] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None

@strawberry.type
class Quantity:
    value: Optional[float] = None
    comparator: Optional[str] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None

    @staticmethod
    def deserialize(json):
        return Quantity(**json)

    @staticmethod
    def filter(instance, input: QuantityInputType):
        return generic_filter(instance, input)