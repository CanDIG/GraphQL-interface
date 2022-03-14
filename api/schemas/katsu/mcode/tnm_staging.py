from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.json_formats.complex_ontology import ComplexOntology, ComplexOntologyInputType
from typing import List, Optional
import strawberry

@strawberry.input
class TNMStagingInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    tnm_type: Optional[str] = None
    stage_group: Optional[ComplexOntologyInputType] = None
    primary_tumor_category: Optional[ComplexOntologyInputType] = None
    regional_nodes_category: Optional[ComplexOntologyInputType] = None
    distant_metastases_category: Optional[ComplexOntologyInputType] = None
    cancer_condition: Optional[str] = None

@strawberry.type
class TNMStaging:
    id: Optional[strawberry.ID] = None
    tnm_type: Optional[str] = None
    stage_group: Optional[ComplexOntology] = None
    primary_tumor_category: Optional[ComplexOntology] = None
    regional_nodes_category: Optional[ComplexOntology] = None
    distant_metastases_category: Optional[ComplexOntology] = None
    cancer_condition: Optional[str] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None


    @staticmethod
    def deserialize(json):
        ret = TNMStaging(**json)
        for (field_name, type) in [("stage_group", ComplexOntology), ("primary_tumor_category", ComplexOntology),\
                                    ("regional_nodes_category", ComplexOntology), ("distant_metastases_category", ComplexOntology)]:
            set_field(json, ret, field_name, type)
        set_extra_properties(json, ret)
        return ret
    
    @staticmethod
    def filter(instance, input: TNMStagingInputType):
        return generic_filter(instance, input)
