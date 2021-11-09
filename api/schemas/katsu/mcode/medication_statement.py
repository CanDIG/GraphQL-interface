from api.interfaces.input import Input
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from typing import List, Optional
import strawberry
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list

@strawberry.input
class MedicationStatementInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    medication_code: Optional[OntologyInputType] = None
    termination_reason: Optional[List[OntologyInputType]] = None
    treatment_intent: Optional[OntologyInputType] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@strawberry.type
class MedicationStatement:
    id: Optional[strawberry.ID] = None
    medication_code: Optional[Ontology] = None
    termination_reason: Optional[List[Ontology]] = None
    treatment_intent: Optional[Ontology] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None


    @staticmethod
    def deserialize(json):
        ret = MedicationStatement(**json)
        for (field_name, type) in [("medication_code", Ontology), ("treatment_intent", Ontology)]:
            set_field(json, ret, field_name, type)
        set_field_list(json, ret, "termination_reason", Ontology)

        set_extra_properties(json, ret)
        return ret

    @staticmethod
    def filter(instance, input: MedicationStatementInputType):
        return generic_filter(instance, input)