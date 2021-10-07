from api.interfaces.input import Input
from api.schemas.diagnosis import DiagnosisInputType
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from api.schemas.scalars.json_scalar import JSONScalar
from typing import List, Optional, Union
import strawberry
from api.schemas.json_formats.age_or_age_range import Age, AgeRange
from api.schemas.json_formats.phenopacket_disease_onset import PhenopacketDiseaseOnsetInputType
from api.schemas.json_formats.ontology import Ontology, OntologyInputType


@strawberry.input
class DiseaseInputType(Input):
    id: Optional[strawberry.ID] = None
    term: Optional[OntologyInputType] = None
    onset: Optional[PhenopacketDiseaseOnsetInputType] = None
    disease_stage: Optional[OntologyInputType] = None
    tnm_finding: Optional[OntologyInputType] = None

@strawberry.type
class Disease:
    id: Optional[strawberry.ID] = None
    term: Optional[Ontology] = None
    onset: Optional[Union[Age, AgeRange, Ontology]] = None
    disease_stage: Optional[List[Ontology]] = None
    tnm_finding: Optional[List[Ontology]] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = Disease(**json)
        
        set_field(json, ret, "term", Ontology)

        onset = json.get("onset")
        if onset != None:
            if onset.get("age") != None:
                ret.onset = Age(onset.get("age"))
            elif onset.get("id") != None:
                ret.onset = Ontology(**onset)
            else:
                ret.onset = AgeRange(**onset)
        
        for (field_name, type) in [("disease_stage", Ontology),("tnm_finding", Ontology)]:
            set_field_list(json, ret, field_name, type)

        set_extra_properties(json, ret)

        return ret

    @staticmethod
    def filter(instance, input: DiseaseInputType):
        return generic_filter(instance, input)