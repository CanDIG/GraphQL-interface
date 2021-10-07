from typing import Any, NewType

import strawberry

JSONScalar = strawberry.scalar(
    NewType("JSONScalar", Any),
    serialize=lambda v: v,
    parse_value=lambda v: v,
    description="The GenericScalar scalar type represents a generic GraphQL scalar value that could be: List or Object."
)
