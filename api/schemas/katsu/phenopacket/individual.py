from api.schemas.dataloader_input import DataLoaderInput, DataLoaderOutput
from api.interfaces.input import Input
from api.schemas.utils import generic_filter, get_katsu_response, set_extra_properties, set_field, set_field_list
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.json_formats.age_or_age_range import Age, AgeRange
from typing import List, Optional, Union
import strawberry
from api.schemas.json_formats.comorbid_condition import ComorbidCondition, ComorbidConditionInputType
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.katsu.phenopacket.biosample import Biosample

@strawberry.input
class IndividualInputType(Input):
    ids: Optional[strawberry.ID] = None
    date_of_birth: Optional[str] = None
    sex: Optional[str] = None
    karyotypic_sex: Optional[str] = None
    taxonomy: Optional[OntologyInputType] = None
    active: Optional[bool] = None
    comorbid_condition: Optional[ComorbidConditionInputType] = None
    ecog_performance_status: Optional[OntologyInputType] = None
    karnofsky: Optional[OntologyInputType] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None

@strawberry.type
class Individual:
    id: Optional[strawberry.ID] = None
    alternate_ids: Optional[List[strawberry.ID]] = None
    date_of_birth: Optional[str] = None
    age: Optional[Union[Age, AgeRange]] = None
    sex: Optional[str] = None
    karyotypic_sex: Optional[str] = None
    taxonomy: Optional[Ontology] = None
    active: Optional[bool] = None
    deceased: Optional[bool] = None
    comorbid_condition: Optional[ComorbidCondition] = None
    ecog_performance_status: Optional[Ontology] = None
    karnofsky: Optional[Ontology] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None
    phenopackets: Optional[JSONScalar] = None
    biosamples: Optional[List[Biosample]] = None

    @staticmethod
    def deserialize(json):
        ret = Individual(**json)
        
        age = json.get("age")
        if age != None:
            if age.get("age") != None:
                ret.age = Age(age.get("age"))
            else:
                ret.age = AgeRange(**age)
        
        for (field_name, type) in [("taxonomy", Ontology), ("comorbid_condition", ComorbidCondition),\
                                    ("ecog_performance_status", Ontology), ("karnofsky", Ontology)]:
            set_field(json, ret, field_name, type)

        set_field_list(json, ret, 'biosamples', Biosample)
        set_extra_properties(json, ret)
        
        return ret

    @staticmethod
    def filter(instance, input: IndividualInputType):
        return generic_filter(instance, input)