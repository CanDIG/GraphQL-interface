from api.interfaces.input import Input
from api.schemas.dataloader_input import DataLoaderOutput
from api.schemas.katsu.mcode.cancer_related_procedure import CancerRelatedProcedure
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.katsu.mcode.medication_statement import MedicationStatement, MedicationStatementInputType
from api.schemas.katsu.mcode.cancer_condition import CancerCondition, CancerConditionInputType
from api.schemas.katsu.mcode.genomics_report import GenomicsReportInputType, GenomicsReport
from api.schemas.katsu.phenopacket.individual import Individual, IndividualInputType
from typing import List, Optional
import strawberry




@strawberry.input
class MCodePacketInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    subject: Optional[IndividualInputType] = None
    genomics_report: Optional[GenomicsReportInputType] = None
    cancer_condition: Optional[List[CancerConditionInputType]] = None
    medication_statement: Optional[List[MedicationStatementInputType]] = None
    date_of_death: Optional[str] = None
    cancer_disease_status: Optional[OntologyInputType] = None
    tanle: Optional[str] = None


@strawberry.type
class MCodePacket:
    id: Optional[strawberry.ID] = None
    subject: Optional[Individual] = None
    genomics_report: Optional[GenomicsReport] = None
    cancer_condition: Optional[List[CancerCondition]] = None
    medication_statement: Optional[List[MedicationStatement]] = None
    date_of_death: Optional[str] = None
    cancer_disease_status: Optional[Ontology] = None
    cancer_related_procedures: Optional[List[CancerRelatedProcedure]] = None
    table: Optional[str] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = MCodePacket(**json)

        for (field_name ,type) in [("subject", Individual), ("genomics_report", GenomicsReport), \
                                ("cancer_disease_status", Ontology)]:
            set_field(json, ret, field_name, type)
        
        set_field_list(json, ret, "cancer_condition", CancerCondition)
        set_field_list(json, ret, "medication_statement", MedicationStatement)
        set_field_list(json, ret, "cancer_related_procedures", CancerRelatedProcedure)

        set_extra_properties(json, ret)

        return ret


    @staticmethod
    def filter(instance, input: MCodePacketInputType):
        return generic_filter(instance, input)