from api.schemas.utils import generic_filter
from api.schemas.json_formats.quantity import Quantity, QuantityInputType
from typing import Optional
import strawberry

@strawberry.input
class RatioInputType:
    numerator: Optional[QuantityInputType] = None
    denominator: Optional[QuantityInputType] = None

@strawberry.type
class Ratio:
    numerator: Optional[Quantity] = None
    denominator: Optional[Quantity] = None

    @staticmethod
    def deserialize(json):
        return Ratio(**json)

    @staticmethod
    def filter(instance, input: RatioInputType):
        return generic_filter(instance, input)