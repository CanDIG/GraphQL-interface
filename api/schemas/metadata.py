from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from api.schemas.json_formats.phenopacket_update import PhenopacketUpdate
from api.schemas.scalars.json_scalar import JSONScalar
from typing import List, Optional
import strawberry
from api.schemas.json_formats.phenopacket_external_reference import PhenopacketExternalReference, PhenopacketExternalReferenceInputType
from api.schemas.katsu.phenopacket.resource import Resource, ResourceInputType

@strawberry.input
class MetaDataInputType(Input):
    id: Optional[strawberry.ID] = None
    resources: Optional[List[ResourceInputType]] = None
    phenopacket_schema_version: Optional[str] = None
    external_references: Optional[PhenopacketExternalReferenceInputType] = None

@strawberry.type
class MetaData:
    id: Optional[strawberry.ID] = None
    created: Optional[str] = None
    created_by: Optional[str] = None
    submitted_by: Optional[str] = None
    resources: Optional[List[Resource]] = None
    updates: Optional[List[PhenopacketUpdate]] = None
    phenopacket_schema_version: Optional[str] = None
    external_references: Optional[List[PhenopacketExternalReference]] = None
    extra_properties: Optional[JSONScalar] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = MetaData(**json)

        for (field_name, type) in [("resources", Resource), ("updates", PhenopacketUpdate), ("external_references", PhenopacketExternalReference)]:
            set_field_list(json, ret, field_name, type)

        set_extra_properties(json, ret)

        return ret

    @staticmethod
    def filter(instance, input: MetaDataInputType):
        return generic_filter(instance, input)