from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_JSON_scalar, set_extra_properties, set_field, set_field_list
from typing import List, Optional
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.scalars.json_scalar import JSONScalar
@strawberry.input
class GenomicRegionStudiedInputType(Input):
    ids: Optional[List[strawberry.ID]]= None
    dna_ranges_examined: Optional[List[OntologyInputType]] = None
    dna_region_description: Optional[List[str]] = None
    gene_studied: Optional[List[OntologyInputType]] = None
    genomic_region_coordinate_system: Optional[OntologyInputType] = None
    
@strawberry.type
class GenomicRegionStudied:
    id: Optional[strawberry.ID] = None
    dna_ranges_examined: Optional[List[Ontology]] = None
    dna_region_description: Optional[List[str]] = None
    gene_mutation: Optional[List[Ontology]] = None
    gene_studied: Optional[List[Ontology]] = None
    genomic_reference_sequence_id: Optional[JSONScalar] = None
    genomic_region_coordinate_system: Optional[Ontology] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = GenomicRegionStudied(**json)

        for (field_name, type) in [("dna_ranges_examined", Ontology), ("gene_mutation", Ontology),\
                                     ("gene_studied", Ontology)]:
            set_field_list(json, ret, field_name, type)

        set_field(json, ret, "genomic_region_coordinate_system", Ontology)

        set_JSON_scalar(json, ret, "genomic_reference_sequence_id")
        
        set_extra_properties(json, ret)

        return ret
    
    @staticmethod
    def filter(instance, input: GenomicRegionStudiedInputType):
        return generic_filter(instance, input)