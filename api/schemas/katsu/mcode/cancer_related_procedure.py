from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.katsu.mcode.cancer_condition import CancerCondition, CancerConditionInputType
from typing import List, Optional
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
@strawberry.input
class CancerRelatedProcedureInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    procedure_type: Optional[str] = None
    code: Optional[OntologyInputType] = None
    body_site: Optional[List[OntologyInputType]] = None
    laterality: Optional[OntologyInputType] = None
    treatment_intent: Optional[OntologyInputType] = None
    reason_code: Optional[OntologyInputType] = None
    reason_reference: Optional[List[CancerConditionInputType]] = None

@strawberry.type
class CancerRelatedProcedure:
    id: Optional[strawberry.ID] = None
    procedure_type: Optional[str] = None
    code: Optional[Ontology] = None
    body_site: Optional[List[Ontology]] = None
    laterality: Optional[Ontology] = None
    treatment_intent: Optional[Ontology] = None
    reason_code: Optional[Ontology] = None
    reason_reference: Optional[List[str]] = None # reason_reference is a list of ids (represented as strings) to cancer conditions
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None


    @staticmethod
    def deserialize(json):
        ret = CancerRelatedProcedure(**json)
        for (field_name, type) in [("code", Ontology), ("laterality", Ontology),\
                                    ("treatment_intent", Ontology), ("reason_code", Ontology)]:
            set_field(json, ret, field_name, type)
        set_field_list(json, ret, "body_site", Ontology)
        set_extra_properties(json, ret)
        return ret
    
    @staticmethod
    def filter(instance, input: CancerRelatedProcedureInputType):
        return generic_filter(instance, input)