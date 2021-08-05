from api.schemas.utils import gene_filter, generic_all_resolver
from api.schemas.variant import Variant, VariantInputType
from api.schemas.resource import ResourceInputType
from api.schemas.procedure import ProcedureInputType
from api.schemas.phenotypicfeature import PhenotypicFeatureInputType
from api.schemas.phenopacket import PhenopacketInputType
from api.schemas.metadata import MetaDataInputType
from api.schemas.interpretation import InterpretationInputType
from api.schemas.individual import IndividualInputType
from api.schemas.htsfile import HtsFileInputType
from api.schemas.genomicinterpretation import GenomicInterpretationInputType
from api.schemas.gene import GeneInputType
from api.schemas.disease import Disease, DiseaseInputType
from api.schemas.diagnosis import DiagnosisInputType
from api.schemas.biosample import BiosampleInputObjectType
from typing import Optional, Union
import strawberry

@strawberry.input
class AggregateQueryInput:
    # filter: Optional[Union[BiosampleInputObjectType, DiagnosisInputType, DiseaseInputType,
    #                 GeneInputType, GenomicInterpretationInputType, HtsFileInputType,
    #                 IndividualInputType, InterpretationInputType, MetaDataInputType, PhenopacketInputType,
    #                 PhenotypicFeatureInputType, ProcedureInputType, ResourceInputType, VariantInputType]] = None
    biosample_filter: Optional[BiosampleInputObjectType] = None
    diagnosis_filter: Optional[DiagnosisInputType] = None
    disease_filter: Optional[DiseaseInputType] = None
    gene_filter: Optional[GeneInputType] = None
    genomic_interpretation_filter: Optional[GenomicInterpretationInputType] = None
    hts_file_filter: Optional[HtsFileInputType] = None
    individual_filter: Optional[IndividualInputType] = None
    interpretation_filter: Optional[InterpretationInputType] = None
    meta_data_filter: Optional[MetaDataInputType] = None
    phenopacket_filter: Optional[PhenopacketInputType] = None
    phenotypic_feature_filter: Optional[PhenotypicFeatureInputType] = None
    procedure_filter: Optional[ProcedureInputType] = None
    resource_filter: Optional[ResourceInputType] = None
    variant_filter: Optional[VariantInputType] = None

@strawberry.type
class AggregateQuery:

    @strawberry.field
    async def count(self, info, aggregate_input: AggregateQueryInput = None) -> int:
        if aggregate_input.phenopacket_filter != None:
            filtered_res = await generic_all_resolver(info, "phenopacket_loader", aggregate_input.phenopacket_filter)
            return len(filtered_res)

    @strawberry.field
    async def ratio(self, info, aggregate_input: AggregateQueryInput = None) -> float:
        if aggregate_input.phenopacket_filter != None:
            filtered_res = await generic_all_resolver(info, "phenopacket_loader", aggregate_input.phenopacket_filter)
        all_res = await generic_all_resolver(info, "phenopacket_loader", None)
        return len(filtered_res)/len(all_res)