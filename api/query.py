from api.schemas.aggregate_query import AggregateQuery
from api.schemas.candig_server.variant import CandigServerVariant, CandigServerVariantDataLoaderInput, CandigServerVariantInput
from api.schemas.utils import filter_results, generic_all_resolver
from typing import List, Optional
import strawberry
from api.schemas.metadata import MetaData
from api.schemas.phenotypicfeature import PhenotypicFeature
from api.schemas.procedure import Procedure
from api.schemas.htsfile import HtsFile
from api.schemas.gene import Gene
from api.schemas.variant import Variant
from api.schemas.disease import Disease
from api.schemas.biosample import Biosample
from api.schemas.phenopacket import Phenopacket, PhenopacketInputType
from api.schemas.genomicinterpretation import GenomicInterpretation
from api.schemas.diagnosis import Diagnosis
# from api.schemas.interpretation import Interpretation

@strawberry.type
class Query:
    # all_meta_data: List[MetaData]
    # all_phenotypic_features: List[PhenotypicFeature]
    # all_procedures: List[Procedure]
    # all_hts_files: List[HtsFile]
    # all_genes: List[Gene]
    # all_variants: List[Variant]
    # all_diseases: List[Disease]
    # all_biosamples: List[Biosample]
    # all_phenopackets: List[Phenopacket]
    # all_genomic_interpretations: List[GenomicInterpretation]
    # all_diagnoses: List[Diagnosis]
    # all_interpretations: List[Interpretation]


    @strawberry.field
    async def all_phenopackets(self, info, input: Optional[PhenopacketInputType] = None) -> List[Phenopacket]:
        res = await generic_all_resolver(info, "phenopacket_loader", input)
        return filter_results(res, input, Phenopacket)
    
    @strawberry.field
    async def candig_server_variants(self, info, input: Optional[CandigServerVariantInput], dataset_name: Optional[str] = None, dataset_id: Optional[str] = None) -> List[CandigServerVariant]:
        return await info.context["candig_server_variants_loader"].load(CandigServerVariantDataLoaderInput(None, input, None))

    @strawberry.field
    async def aggregate(self, info) -> AggregateQuery:
        return AggregateQuery()