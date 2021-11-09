from api.schemas.utils import filter_results, generic_resolver, generic_resolver_helper
from typing import List, Optional
from api.schemas.metadata import MetaData
import strawberry
from api.schemas.katsu.phenopacket.phenotypicfeature import PhenotypicFeature
from api.schemas.katsu.phenopacket.procedure import Procedure
from api.schemas.katsu.phenopacket.htsfile import HtsFile
from api.schemas.katsu.phenopacket.gene import Gene
from api.schemas.katsu.phenopacket.variant import Variant
from api.schemas.katsu.phenopacket.disease import Disease
from api.schemas.katsu.phenopacket.biosample import Biosample
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket, PhenopacketInputType
from api.schemas.katsu.phenopacket.genomicinterpretation import GenomicInterpretation
from api.schemas.katsu.phenopacket.diagnosis import Diagnosis
from api.schemas.katsu.phenopacket.interpretation import Interpretation

@strawberry.type
class PhenopacketDataModels:
    # all_meta_data: List[MetaData]
    # all_phenotypic_features: List[PhenotypicFeature]
    # all_procedures: List[Procedure]
    # all_hts_files: List[HtsFile]
    # all_genes: List[Gene]
    # all_variants: List[Variant]
    # all_diseases: List[Disease]
    # all_biosamples: List[Biosample]
    # all_genomic_interpretations: List[GenomicInterpretation]
    # all_diagnoses: List[Diagnosis]
    # all_interpretations: List[Interpretation]

    @strawberry.field
    async def phenopackets(self, info, input: Optional[PhenopacketInputType] = None) -> List[Phenopacket]:
        res = await generic_resolver(info, "phenopackets_loader", input.ids, Phenopacket)
        return res