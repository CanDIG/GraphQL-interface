from api.schemas.katsu.mcode.genomic_region_studied import GenomicRegionStudied
from api.schemas.scalars.json_scalar import JSONScalar
from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_extra_properties, set_field, set_field_list
from api.schemas.katsu.mcode.cancer_genetic_variant import CancerGeneticVariant, CancerGeneticVariantInputType
from api.schemas.katsu.mcode.genetic_specimen import GeneticSpecimen, GeneticSpecimenInputType
from typing import List, Optional
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType

@strawberry.input
class GenomicsReportInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
    code: Optional[OntologyInputType] = None
    performing_organization_name: Optional[str] = None
    issued: Optional[str] = None
    genetic_speciment: Optional[GeneticSpecimenInputType] = None
    genetic_variant: Optional[CancerGeneticVariantInputType] = None

@strawberry.type
class GenomicsReport:
    id: Optional[strawberry.ID] = None
    code: Optional[Ontology] = None
    performing_organization_name: Optional[str] = None
    issued: Optional[str] = None
    genetic_specimen: Optional[List[GeneticSpecimen]] = None
    genetic_variant: Optional[CancerGeneticVariant] = None
    genomic_region_studied: Optional[GenomicRegionStudied] = None
    extra_properties: Optional[JSONScalar] = None
    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def deserialize(json):
        ret = GenomicsReport(**json)

        for (field_name, type) in [
            ("code", Ontology), ("genetic_variant", CancerGeneticVariant), ("genomic_region_studied", GenomicRegionStudied)]:
            set_field(json, ret, field_name, type)
        set_field_list(json, ret, "genetic_specimen", GeneticSpecimen)
        set_extra_properties(json, ret)
        return ret

    @staticmethod
    def filter(instance, input: GenomicsReportInputType):
        return generic_filter(instance, input)