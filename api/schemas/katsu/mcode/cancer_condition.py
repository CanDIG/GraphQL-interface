from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from typing import List, Optional
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
import strawberry
from api.schemas.scalars.json_scalar import JSONScalar

@strawberry.input
class CancerConditionInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    condition_type: Optional[str] = None
    body_site: Optional[List[OntologyInputType]] = None
    laterality: Optional[OntologyInputType] = None
    clinical_status: Optional[OntologyInputType] = None
    code: Optional[OntologyInputType] = None
    date_of_diagnosis: Optional[str] = None
    histology_morphology_behavior: Optional[OntologyInputType] = None
    verification_status: Optional[OntologyInputType] = None



@strawberry.type
class CancerCondition:
    id: Optional[strawberry.ID] = None
    condition_type: Optional[str] = None
    body_site: Optional[List[Ontology]] = None
    laterality: Optional[Ontology] = None
    clinical_status: Optional[Ontology] = None
    code: Optional[Ontology] = None
    date_of_diagnosis: Optional[str] = None
    histology_morphology_behavior: Optional[Ontology] = None
    verification_status: Optional[Ontology] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = CancerCondition(**json)
        
        for (field_name, type) in [("laterality", Ontology), ("clinical_status", Ontology),\
                                    ("code", Ontology), ("histology_morphology_behavior", Ontology),\
                                    ("verification_status", Ontology)]:
            set_field(json, ret, field_name, type)
        set_field_list(json, ret, "body_site", Ontology)
        set_extra_properties(json, ret)
        
        return ret

    @staticmethod
    def filter(instance, input: CancerConditionInputType):
        return generic_filter(instance, input)