from api.schemas.dataloader_input import DataLoaderInput
from api.schemas.utils import get_token
from typing import List
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
from api.schemas.interpretation import Interpretation

@strawberry.type
class Query:
    all_meta_data: List(MetaData)
    all_phenotypic_features: List(PhenotypicFeature)
    all_procedures: List(Procedure)
    all_hts_files: List(HtsFile)
    all_genes: List(Gene)
    all_variants: List(Variant)
    all_diseases: List(Disease)
    all_biosamples: List(Biosample)
    all_phenopackets: List(Phenopacket)
    all_genomic_interpretations: List(GenomicInterpretation)
    all_diagnoses: List(Diagnosis)
    all_interpretations: List(Interpretation)

    @strawberry.field
    async def all_phenopackets(self, info, input = PhenopacketInputType) -> Phenopacket:
        token = get_token(info)
        if input == None:
            ids = None
        else:
            ids = input.get("ids")
        return await info.context["phenopacket_loader"].load(DataLoaderInput(token, ids))