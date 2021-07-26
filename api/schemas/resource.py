from api.schemas.scalars.json_scalar import JSONScalar
import strawberry

@strawberry.input
class ResourceInputType:
    id: id
    name: str
    namespace_prefix: str
    url: str
    version: str
    iri_prefix: str

@strawberry.type
class Resource:
    id: id
    name: str
    namespace_prefix: str
    url: str
    version: str
    iri_prefix: str
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def extra_properties(self, info):
        return self.extra_properties