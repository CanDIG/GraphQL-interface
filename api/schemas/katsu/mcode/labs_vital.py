from api.interfaces.input import Input
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.json_formats.ratio import Ratio, RatioInputType
from api.schemas.json_formats.quantity import Quantity, QuantityInputType
from api.schemas.utils import generic_filter, set_extra_properties, set_field
from api.schemas.katsu.phenopacket.individual import Individual, IndividualInputType
from typing import List, Optional, Union
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType

@strawberry.input
class LabsVitalInputType(Input):
    ids: Optional[List[strawberry.ID]]= None
    individual: Optional[IndividualInputType] = None
    tumor_marker_code: Optional[OntologyInputType] = None
    tumor_marker_data_value_ratio: Optional[RatioInputType] = None
    tumor_marker_data_value_quantity: Optional[QuantityInputType] = None
    tumor_marker_data_value_ontology: Optional[OntologyInputType] = None

@strawberry.type
class LabsVital:
    id: Optional[strawberry.ID] = None
    individual: Optional[Individual] = None
    tumor_marker_code: Optional[Ontology] = None
    tumor_marker_data_value: Optional[Union[Quantity, Ratio, Ontology]] = None #TUMOR_MARKER_DATA_VALUE in katsu json schemas
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = LabsVital(**json)

        for (field_name, type) in [("individual", Individual), ("tumor_marker_code", Ontology)]:
            set_field(json, ret, field_name, type)

        if ret.tumor_marker_data_value:
            if ret.tumor_marker_data_value.get("code"):
                set_field(json, ret, "tumor_marker_data_value", Quantity)
            elif ret.tumor_marker_data_value.get("numerator"):
                set_field(json, ret, "tumor_marker_data_value", Ratio)
            elif ret.tumor_marker_data_value.get("id"):
                set_field(json, ret, "tumor_marker_data_value", Ontology)
        
        set_extra_properties(json, ret)

        return ret
    

    @staticmethod
    def filter(instance, input: LabsVitalInputType):
        ret = generic_filter(instance, input)
        return ret and Quantity.filter(instance.tumor_marker_data_value, input.tumor_marker_data_value_quantity)\
                    and Ratio.filter(instance.tumor_marker_data_value, input.tumor_marker_data_value_ratio)\
                    and Ontology.filter(instance.tumor_marker_data_value, input.tumor_marker_data_value_ontology)
