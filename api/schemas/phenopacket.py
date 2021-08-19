from api.schemas.candig_server.variant import CandigServerVariant, CandigServerVariantDataLoaderInput, CandigServerVariantInput
from api.interfaces.input import Input
from typing import List, Optional
import strawberry

from strawberry.field import field
from api.schemas.dataloader_input import DataLoaderOutput
from api.schemas.utils import (
    generic_filter,
    get_katsu_response,
    set_extra_properties,
    set_field,
    set_field_list
)
from api.schemas.individual import Individual, IndividualInputType
from api.schemas.phenotypicfeature import PhenotypicFeature, PhenotypicFeatureInputType
from api.schemas.biosample import Biosample, BiosampleInputObjectType
from api.schemas.disease import Disease, DiseaseInputType
from api.schemas.gene import Gene, GeneInputType
from api.schemas.variant import Variant, VariantInputType
from api.schemas.htsfile import HtsFile, HtsFileInputType
from api.schemas.metadata import MetaData, MetaDataInputType
from api.schemas.scalars.json_scalar import JSONScalar


async def get_phenopackets(param):
    ret = []
    for dataloader_input in param:
        token = dataloader_input.token
        if dataloader_input.ids == None:
            response = get_katsu_response("phenopackets", token)
            obj_arr = list()
            for p in response["results"]:
                obj_arr.append(Phenopacket.deserialize(p))
        else:
            ids = set(dataloader_input.ids)
            obj_arr = list()
            for id in ids:
                obj_arr.append(Phenopacket.deserialize(get_katsu_response(f"phenopackets/{id}", token)))
        ret.append(DataLoaderOutput(obj_arr))
    return ret

@strawberry.input
class PhenopacketInputType(Input):
    ids: Optional[List[strawberry.ID]] = None
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
    id: strawberry.ID = None
    subject: Optional[Individual] = None
    phenotypic_features: Optional[List[PhenotypicFeature]] = None
    biosamples: Optional[List[Biosample]] = None
    genes: Optional[List[Gene]] = None
    variants: Optional[List[Variant]] = None
    diseases: Optional[List[Disease]] = None
    hts_files: Optional[List[HtsFile]] = None
    meta_data: Optional[MetaData] = None
    table: Optional[str] = None
    created: Optional[str] = None
    updated: Optional[str] = None
    extra_properties: Optional[JSONScalar] = None


    @strawberry.field
    async def candig_server_variants(self, info, input: Optional[CandigServerVariantInput] = None) -> List[CandigServerVariant]:
        res = await info.context["candig_server_variants_loader"].load(CandigServerVariantDataLoaderInput(None, input, self.id))
        return res

    @staticmethod
    def deserialize(json):
        ret = Phenopacket(**json)

        for (field_name ,type) in [("phenotypic_features", PhenotypicFeature), ("biosamples", Biosample), \
                                ("genes", Gene), ("variants", Variant), ("diseases", Disease), \
                                ("hts_files", HtsFile)]:
            set_field_list(json, ret, field_name, type)
        
        set_field(json, ret, "metadata", MetaData)
        set_field(json, ret, "subject", Individual)

        set_extra_properties(json, ret)

        return ret


    @staticmethod
    def filter(instance, input):
        return generic_filter(instance, input)
