from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from typing import List, Optional
import strawberry
import uuid
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.scalars.json_scalar import JSONScalar

@strawberry.input
class PhenotypicFeatureInputType(Input):
    id: Optional[strawberry.ID] = None
    description: Optional[str] = None
    type: Optional[OntologyInputType] = None
    negated: Optional[bool] = None
    severity: Optional[OntologyInputType] = None
    modifier: Optional[List[OntologyInputType]] = None
    onset: Optional[OntologyInputType] = None
    evidence: Optional[OntologyInputType] = None
    biosample: Optional[str] = None
    phenopacket: Optional[str] = None
    

@strawberry.type
class PhenotypicFeature:
    id: Optional[strawberry.ID] = None
    description: Optional[str] = None
    type: Optional[Ontology] = None
    negated: Optional[bool] = None
    severity: Optional[Ontology] = None
    modifier: Optional[List[Ontology]] = None
    onset: Optional[Ontology] = None
    evidence: Optional[Ontology] = None
    biosample: Optional[str] = None
    phenopacket: Optional[str] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = PhenotypicFeature(**json)

        for (field_name ,type) in [("type", Ontology), ("severity", Ontology), \
                                ("onset", Ontology), ("evidence", Ontology)]:
            set_field(json, ret, field_name, type)

        set_field_list(json, ret, "modifier", Ontology)

        set_extra_properties(json, ret)

        return ret

    @staticmethod
    def filter(instance, input: PhenotypicFeatureInputType):
        return generic_filter(instance, input)