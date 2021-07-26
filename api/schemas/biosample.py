from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.json_formats.age_or_age_range import Age, AgeRange
from typing import List, Union
from api.schemas.json_formats.ontology import SampleTissue, SampleTissueInputType
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.json_formats.age_or_age_range import AgeInputType
from api.schemas.phenotypicfeature import PhenotypicFeature, PhenotypicFeatureInputType
from api.schemas.procedure import Procedure, ProcedureInputType
from api.schemas.variant import Variant, VariantInputType

@strawberry.input
class BiosampleInputObjectType:
    id: id
    phenotypic_features: PhenotypicFeatureInputType
    individual: str
    description: str
    sampled_tissue: SampleTissueInputType
    taxonomy: OntologyInputType
    individual_age_at_collection: AgeInputType
    histological_diagnosis: OntologyInputType
    tumor_progression: OntologyInputType
    tumor_grade: OntologyInputType
    diagnostic_markers: OntologyInputType
    procedure: ProcedureInputType
    hts_file: List(str)
    variant = List(VariantInputType)
    is_control_sample = bool
    
@strawberry.type
class Biosample:
    id: id
    phenotypic_features: List(PhenotypicFeature)
    individual: str
    description: str
    sampled_tissue: SampleTissue
    taxonomy: Ontology
    individual_age_at_collection: Union[Age, AgeRange]
    histological_diagnosis: Ontology
    tumor_progression: Ontology
    tumor_grade: Ontology
    diagnostic_markers: Ontology
    procedure: Procedure
    hts_files: List(str)
    variants: List(Variant)
    is_control_sample: bool
    extra_properties: JSONScalar
    created: str
    updated: str
    
    @strawberry.field
    def procedure(self, info) -> Procedure:
        return self.procedure

    @strawberry.field
    def phenotypic_features(self, info) -> PhenotypicFeature:
        return self.phenotypic_features

    @strawberry.field
    def sampled_tissue(self, info) -> SampleTissue:
        return self.sampled_tissue

    @strawberry.field
    def individual_age_at_collection(self, info) -> Union[Age, AgeRange]:
        return self.individual_age_at_collection

    @strawberry.field
    def histological_diagnosis(self, info) -> Ontology:
        return self.histological_diagnosis

    @strawberry.field
    def tumor_progression(self, info) -> Ontology:
        return self.tumor_progression

    @strawberry.field
    def tumor_grade(self, info) -> Ontology:
        return self.tumor_grade

    @strawberry.field
    def diagnostic_markers(self, info) -> Ontology:
        return self.diagnostic_markers

    @strawberry.field
    def procedure(self, info) -> Procedure:
        return self.procedure

    @strawberry.field
    def hts_files(self, info) -> List(str):
        return self.hts_files

    @strawberry.field
    def variants(self, info) -> List(Variant):
        return self.variants

    @strawberry.field
    def is_control_sample(self, info) -> bool:
        return self.is_control_sample
    
    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties