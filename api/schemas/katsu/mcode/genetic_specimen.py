from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from typing import List, Optional
import strawberry
from api.schemas.scalars.json_scalar import JSONScalar

@strawberry.input
class GeneticSpecimenInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    specimen_type: Optional[OntologyInputType] = None
    collection_body: Optional[OntologyInputType] = None
    laterality: Optional[OntologyInputType] = None

@strawberry.type
class GeneticSpecimen:
    id: Optional[strawberry.ID] = None
    specimen_type: Optional[Ontology] = None
    collection_body: Optional[Ontology] = None
    laterality: Optional[Ontology] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = GeneticSpecimen(**json)
        
        for (field_name, type) in [("specimen_type", Ontology), ("collection_body", Ontology),\
                                    ("laterality", Ontology)]:
            set_field(json, ret, field_name, type)
        
        set_extra_properties(json, ret)

        return ret
    
    @staticmethod
    def filter(instance, input: GeneticSpecimenInputType):
        return generic_filter(instance, input)