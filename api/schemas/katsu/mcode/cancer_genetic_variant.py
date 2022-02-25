from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.schemas.katsu.phenopacket.gene import Gene, GeneInputType
from typing import List, Optional
import strawberry

@strawberry.input
class CancerGeneticVariantInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    data_value: Optional[OntologyInputType] = None
    method: Optional[OntologyInputType] = None
    amino_acid_change: Optional[OntologyInputType] = None
    amino_acid_change_type: Optional[OntologyInputType] = None
    cytogenetic_location: Optional[OntologyInputType] = None
    cytogenetic_nomenclature: Optional[OntologyInputType] = None
    gene_studied: Optional[GeneInputType] = None
    genomic_dna_change: Optional[OntologyInputType] = None
    genomic_source_class: Optional[OntologyInputType] = None
    variation_code: Optional[OntologyInputType] = None

@strawberry.type
class CancerGeneticVariant:
    id: Optional[strawberry.ID] = None
    data_value: Optional[Ontology] = None
    method: Optional[Ontology] = None
    amino_acid_change: Optional[Ontology] = None
    amino_acid_change_type: Optional[Ontology] = None
    cytogenetic_location: Optional[Ontology] = None
    cytogenetic_nomenclature: Optional[Ontology] = None
    gene_studied: Optional[List[Gene]] = None
    genomic_dna_change: Optional[Ontology] = None
    genomic_source_class: Optional[Ontology] = None
    variation_code: Optional[List[Ontology]] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = CancerGeneticVariant(**json)
        
        for (field_name, type) in [("data_value", Ontology), ("method", Ontology),\
                                    ("amino_acid_change", Ontology), ("amino_acid_change_type", Ontology),\
                                    ("cytogenetic_location", Ontology), ("cytogenetic_nomenclature", Ontology),\
                                    ("genomic_dna_change", Ontology), ("genomic_source_class", Ontology)]:
            set_field(json, ret, field_name, type)

        if isinstance(json["variation_code"], List):
            set_field_list(json, ret, "variation_code", Ontology)
        else:
            set_field(json, ret, "variation_code", Ontology)
            
        set_field_list(json, ret, "gene_studied", Gene)
        set_extra_properties(json, ret)
        
        return ret

    @staticmethod
    def filter(instance, input: CancerGeneticVariantInputType):
        return generic_filter(instance, input)
