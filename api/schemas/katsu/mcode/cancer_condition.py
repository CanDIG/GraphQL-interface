

from typing import List, Optional
import strawberry
from api.interfaces.input import Input
from api.schemas.json_formats.complex_ontology import ComplexOntology, ComplexOntologyInputType
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list

@strawberry.input
class CancerConditionTNMStagingInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    tnm_type: Optional[str] = None
    stage_group: Optional[ComplexOntologyInputType] = None
    primary_tumor_category: Optional[ComplexOntologyInputType] = None
    regional_nodes_category: Optional[ComplexOntologyInputType] = None
    distant_metastases_category: Optional[ComplexOntologyInputType] = None

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
class CancerConditionTNMStaging:
    id: Optional[strawberry.ID] = None
    tnm_type: Optional[str] = None
    stage_group: Optional[ComplexOntology] = None
    primary_tumor_category: Optional[ComplexOntology] = None
    regional_nodes_category: Optional[ComplexOntology] = None
    distant_metastases_category: Optional[ComplexOntology] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = CancerConditionTNMStaging(**json)
        for (field_name, type) in [("stage_group", ComplexOntology), ("primary_tumor_category", ComplexOntology),\
                                    ("regional_nodes_category", ComplexOntology), ("distant_metastases_category", ComplexOntology)]:
            set_field(json, ret, field_name, type)
        set_extra_properties(json, ret)
        return ret
    
    @staticmethod
    def filter(instance, input: CancerConditionTNMStagingInputType):
        return generic_filter(instance, input)

@strawberry.type
class CancerCondition:
    id: Optional[strawberry.ID] = None
    tnm_staging: Optional[List[CancerConditionTNMStaging]] = None
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
        # from api.schemas.katsu.mcode.tnm_staging import TNMStaging
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