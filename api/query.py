from api.schemas.katsu.mcode.mcode_data_models import McodeDataModels
from api.schemas.katsu.katsu_data_models import KatsuDataModels
from api.schemas.aggregate_query import AggregateQuery
from api.schemas.beacon.beacon_data_models import BeaconAlleleDataLoaderInput, BeaconAlleleRequest, BeaconAlleleResponse
from api.schemas.candig_server.variant import CandigServerVariant, CandigServerVariantDataLoaderInput, CandigServerVariantInput
from api.schemas.utils import filter_results, generic_resolver_helper
from typing import List, Optional
import strawberry
from api.schemas.metadata import MetaData

# from api.schemas.interpretation import Interpretation

@strawberry.type 
class Query:
    @strawberry.field
    async def katsu_data_models(self, info) -> KatsuDataModels:
        return KatsuDataModels()

    @strawberry.field
    async def candig_server_variants(self, info, input: Optional[CandigServerVariantInput], dataset_name: Optional[str] = None, dataset_id: Optional[str] = None) -> List[CandigServerVariant]:
        return await info.context["candig_server_variants_loader"].load(CandigServerVariantDataLoaderInput(None, input, None))

    @strawberry.field
    async def aggregate(self, info) -> AggregateQuery:
        return AggregateQuery()
    
    @strawberry.field
    async def beaconQuery(self, info, input: Optional[BeaconAlleleRequest]) -> BeaconAlleleResponse:
        return await info.context['beacon_allele_response_loader'].load(BeaconAlleleDataLoaderInput(input, info))