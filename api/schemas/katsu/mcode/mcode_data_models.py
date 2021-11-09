from api.schemas.utils import generic_resolver
from api.schemas.katsu.mcode.mcode_packet import MCodePacket, MCodePacketInputType
from api.schemas.katsu.mcode.medication_statement import MedicationStatement, MedicationStatementInputType
from api.schemas.katsu.mcode.cancer_related_procedure import CancerRelatedProcedure, CancerRelatedProcedureInputType
from api.schemas.katsu.mcode.tnm_staging import TNMStaging, TNMStagingInputType
from api.schemas.katsu.mcode.genomics_report import GenomicsReportInputType, GenomicsReport
from api.schemas.katsu.mcode.labs_vital import LabsVital, LabsVitalInputType
from api.schemas.katsu.mcode.genomic_region_studied import GenomicRegionStudied, GenomicRegionStudiedInputType
from api.schemas.katsu.mcode.genetic_specimen import GeneticSpecimen, GeneticSpecimenInputType
from api.schemas.katsu.mcode.cancer_genetic_variant import CancerGeneticVariant
from api.schemas.katsu.mcode.cancer_condition import CancerCondition, CancerConditionInputType
from typing import List, Optional
import strawberry

@strawberry.type
class McodeDataModels:
    @strawberry.field
    async def genetic_specimens(self, info, input: Optional[GeneticSpecimenInputType] = None) -> List[GeneticSpecimen]:
        return await generic_resolver(info, "mcode_genetic_specimens", input, GeneticSpecimen)

    @strawberry.field
    async def genomic_regions_studied(self, info, input: Optional[GenomicRegionStudiedInputType] = None) -> List[GenomicRegionStudied]:
        return await generic_resolver(info, "mcode_genomic_regions_studied", input, GenomicsReport)

    @strawberry.field
    async def genomics_reports(self, info, input: Optional[GenomicsReportInputType] = None) -> List[GenomicsReport]:
        return await generic_resolver(info, "mcode_genomics_reports", input, GenomicsReport)

    @strawberry.field
    async def labs_vital(self, info, input: Optional[LabsVitalInputType] = None) -> List[LabsVital]:
        return await generic_resolver(info, "mcode_labs_vital", input, LabsVital)

    @strawberry.field
    async def cancer_conditions(self, info, input: Optional[CancerConditionInputType] = None) -> List[CancerCondition]:
        return await generic_resolver(info, "mcode_cancer_conditions", input, CancerCondition)

    @strawberry.field
    async def TNM_staging(self, info, input: Optional[TNMStagingInputType] = None) -> List[TNMStaging]:
        return await generic_resolver(info, "mcode_tnm_staging_loader", input, TNMStaging)

    @strawberry.field
    async def cancer_related_procedures(self, info, input: Optional[CancerRelatedProcedureInputType] = None) -> List[CancerRelatedProcedure]:
        return await generic_resolver(info, "mcode_cancer_related_procedures_packets_loader", input, CancerRelatedProcedure)

    @strawberry.field
    async def medication_statements(self, info, input: Optional[MedicationStatementInputType] = None) -> List[MedicationStatement]:
        return await generic_resolver(info, "mcode_medication_statements_packets_loader", input, MedicationStatement)

    @strawberry.field
    async def mcode_packets(self, info, input: Optional[MCodePacketInputType] = None) -> List[MCodePacket]:
        return await generic_resolver(info, "mcode_packets_loader", input, MCodePacket)
