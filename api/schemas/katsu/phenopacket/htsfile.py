from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties
from typing import Optional
from api.schemas.scalars.json_scalar import JSONScalar
import strawberry

@strawberry.input
class HtsFileInputType(Input):
    uri: Optional[str] = None
    description: Optional[str] = None
    hts_format: Optional[str] = None
    genome_assembly: Optional[str] = None

@strawberry.type
class HtsFile:
    uri: str
    hts_format: str
    genome_assembly: str
    description: Optional[str] = None
    individual_to_sample_identifiers: Optional[JSONScalar] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = HtsFile(**json)
        individual_to_sample_identifiers = json.get("individual_to_sample_identifiers")
        if individual_to_sample_identifiers != None:
            ret.individual_to_sample_identifiers = JSONScalar(individual_to_sample_identifiers)
        
        set_extra_properties(json, ret)
        
        return ret

    @staticmethod
    def filter(instance, input: HtsFileInputType):
        return generic_filter(instance, input)