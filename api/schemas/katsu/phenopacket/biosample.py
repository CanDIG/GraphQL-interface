from api.interfaces.input import Input
from strawberry.field import field
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.json_formats.age_or_age_range import Age, AgeRange
from typing import List, Optional, Union
from api.schemas.json_formats.ontology import SampleTissue, SampleTissueInputType
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.json_formats.age_or_age_range import AgeInputType
from api.schemas.katsu.phenopacket.phenotypicfeature import PhenotypicFeature, PhenotypicFeatureInputType
from api.schemas.katsu.phenopacket.procedure import Procedure, ProcedureInputType
from api.schemas.katsu.phenopacket.variant import Variant, VariantInputType

@strawberry.input
class BiosampleInputObjectType(Input):
    id: Optional[strawberry.ID] = None
    phenotypic_features: Optional[PhenotypicFeatureInputType] = None
    individual: Optional[str] = None
    description: Optional[str] = None
    sampled_tissue: Optional[SampleTissueInputType] = None
    taxonomy: Optional[OntologyInputType] = None
    individual_age_at_collection: Optional[AgeInputType] = None
    histological_diagnosis: Optional[OntologyInputType] = None
    tumor_progression: Optional[OntologyInputType] = None
    tumor_grade: Optional[OntologyInputType] = None
    diagnostic_markers: Optional[OntologyInputType] = None
    procedure: Optional[ProcedureInputType] = None
    hts_file: Optional[List[str]] = None
    variant: Optional[List[VariantInputType]] = None
    is_control_sample: Optional[bool] = None
    
@strawberry.type
class Biosample:
    id: Optional[strawberry.ID] = None
    phenotypic_features: Optional[List[PhenotypicFeature]] = None
    individual: Optional[str] = None
    description: Optional[str] = None
    sampled_tissue: Optional[SampleTissue] = None
    taxonomy: Optional[Ontology] = None
    individual_age_at_collection: Union[Age, AgeRange] = None
    histological_diagnosis: Optional[Ontology] = None
    tumor_progression: Optional[Ontology] = None
    tumor_grade: Optional[Ontology] = None
    diagnostic_markers: Optional[List[Ontology]] = None
    procedure: Optional[Procedure] = None
    hts_files: Optional[List[str]] = None
    variants: Optional[List[Variant]] = None
    is_control_sample: Optional[bool] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = Biosample(**json)
        
        for (field_name, type) in [("phenotypic_features", PhenotypicFeature), ("variants", Variant), ("diagnostic_markers", Ontology)]:
            set_field_list(json, ret, field_name, type)

        for (field_name, type) in [("sampled_tissue", SampleTissue), ("taxonomy", Ontology), ("histological_diagnosis", Ontology),
                                    ("tumor_progression", Ontology), ("tumor_grade", Ontology), ("procedure", Procedure)]:
            set_field(json, ret, field_name, type)
        
        individual_age_at_collection = json.get("individual_age_at_collection")
        if individual_age_at_collection != None:
            if individual_age_at_collection.get("age") != None:
                set_field(json, ret, 'individual_age_at_collection', Age)
            else:
                set_field(json, ret, 'individual_age_at_collection', AgeRange)

        set_extra_properties(json, ret)
        
        return ret

    @staticmethod
    def filter(instance, input: BiosampleInputObjectType):
        return generic_filter(instance, input)