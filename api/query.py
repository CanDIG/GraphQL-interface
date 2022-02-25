from api.schemas.katsu.katsu_data_models import KatsuDataModels
from api.schemas.aggregate_query import AggregateQuery
from api.schemas.beacon.beacon_data_models import BeaconAlleleDataLoaderInput, BeaconAlleleRequest, BeaconAlleleResponse
from api.schemas.candig_server.variant import CandigServerVariant, CandigServerVariantDataLoaderInput, CandigServerVariantInput
from typing import List, Optional
import strawberry

beacon_base_description = '''
Beacon V1 Endpoint: Returns a BeaconAlleleResponse object, similar in style to the response generated by a Beacon V1 REST API. 
This is used to query Katsu and CanDIG for variants of interest with clinical data present.
'''

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
    
    @strawberry.field(description=beacon_base_description)
    async def beaconQuery(self, info, input: Optional[BeaconAlleleRequest]) -> BeaconAlleleResponse:
        return await info.context['beacon_allele_response_loader'].load(BeaconAlleleDataLoaderInput(input, info))