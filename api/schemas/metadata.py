from api.schemas.scalars.json_scalar import JSONScalar
from typing import List
import strawberry
from api.schemas.json_formats.phenopacket_external_reference import PhenopacketExternalReference, PhenopacketExternalReferenceInputType
from api.schemas.resource import Resource, ResourceInputType

@strawberry.input
class MetaDataInputType:
    id: id
    resources: List(ResourceInputType)
    phenopacket_schema_version: str
    external_references: PhenopacketExternalReferenceInputType

@strawberry.type
class MetaData:
    id: id
    created: str
    created_by: str
    submitted_by: str
    resources: List(Resource)
    updates: JSONScalar
    phenopacket_schema_version: str
    external_references: PhenopacketExternalReference
    extra_properties: JSONScalar
    updated: str

    @strawberry.field
    def resources(self, info) -> List(Resource):
        return self.resources
    
    @strawberry.field
    def updates(self, info) -> JSONScalar:
        return self.updates
    
    @strawberry.field
    def external_references(self, info) -> PhenopacketExternalReference:
        return self.external_references
    
    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties