from typing import List, Optional
import strawberry
from api.schemas.dataloader_input import DataLoaderOutput
from api.schemas.utils import (
    get_response,
    json_to_obj_arr
)
from api.schemas.individual import Individual, IndividualInputType, filter_individual
from api.schemas.phenotypicfeature import PhenotypicFeature, PhenotypicFeatureInputType
from api.schemas.biosample import Biosample, BiosampleInputObjectType
from api.schemas.disease import Disease, DiseaseInputType
from api.schemas.gene import Gene, GeneInputType
from api.schemas.variant import Variant, VariantInputType
from api.schemas.htsfile import HtsFile, HtsFileInputType
from api.schemas.metadata import MetaData, MetaDataInputType
from api.schemas.scalars.json_scalar import JSONScalar


async def get_phenopackets(dataloader_input):
    token = dataloader_input.token
    if dataloader_input.ids == None:
        response = get_response("phenopackets", token)
        obj_arr = json_to_obj_arr(response["results"], Phenopacket)
        return DataLoaderOutput(obj_arr)
    else:
        ids = set(dataloader_input.ids)
        obj_arr = []
        for id in ids:
            obj_arr.append(Phenopacket(**get_response(f"phenopackets/{id}", token)))
        return DataLoaderOutput(obj_arr)


@strawberry.input
class PhenopacketInputType:
    ids: Optional[List(id)] = None
    subject: Optional[IndividualInputType] = None
    phenotypic_features: Optional[PhenotypicFeatureInputType] = None
    biosamples: Optional[BiosampleInputObjectType] = None
    genes: Optional[GeneInputType] = None
    variants: Optional[VariantInputType] = None
    diseases: Optional[DiseaseInputType] = None
    hts_files: Optional[HtsFileInputType] = None
    meta_data: Optional[MetaDataInputType] = None


@strawberry.type
class Phenopacket:
    id: id
    subject: Individual
    phenotypic_features: List(PhenotypicFeature)
    biosamples: List(Biosample)
    genes: List(Gene)
    variants: List(Variant)
    diseases: List(Disease)
    hts_files: List(HtsFile)
    meta_data: MetaData
    table: str
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def subject(self, info) -> Individual:
        return self.subject

    @strawberry.field
    def phenotypic_features(self, info) -> List(PhenotypicFeature):
        return self.phenotypic_features

    @strawberry.field
    def biosamples(self, info) -> List(Biosample):
        return self.biosamples

    @strawberry.field
    def genes(self, info) -> List(Gene):
        return self.genes

    @strawberry.field
    def variants(self, info) -> List(Variant):
        return self.variants

    @strawberry.field
    def diseases(self, info) -> List(Disease):
        return self.diseases

    @strawberry.field
    def hts_files(self, info) -> List(HtsFile):
        return self.hts_files

    @strawberry.field
    def meta_data(self, info) -> MetaData:
        return self.meta_data


def filter_phenopackets(instance, input):
    if input.get("ids") != None:
        return instance.id in input.ids and filter_individual(
            instance.subject, input.subject
        )
    else:
        return filter_individual(instance.subject, input.subject)
