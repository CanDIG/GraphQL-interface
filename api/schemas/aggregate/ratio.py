from api.schemas.katsu.phenopacket.phenopacket import PhenopacketInputType
from api.schemas.aggregate.aggregate_classes import AggregateQueryFilter
from api.schemas.candig_server.variant import CandigServerVariantInput
from api.schemas.katsu.mcode.mcode_packet import MCodePacketInputType

async def get_phenopacket_ratio(info, aggregate_filter, count):
    full_query = AggregateQueryFilter(phenopacket_filter=PhenopacketInputType())
    return await get_query_ratio(info, aggregate_filter, count, full_query)

async def get_mcodepacket_ratio(info, aggregate_filter, count):
    full_query = AggregateQueryFilter(mcodepacket_filter=MCodePacketInputType())
    return await get_query_ratio(info, aggregate_filter, count, full_query)

async def get_variants_ratio(info, aggregate_filter, count):
    full_query = AggregateQueryFilter(
        variant_filter=CandigServerVariantInput(
                start=aggregate_filter.variant_filter.start, 
                end=aggregate_filter.variant_filter.end, 
                referenceName=aggregate_filter.variant_filter.referenceName
            )
        )
    return await get_query_ratio(info, aggregate_filter, count, full_query)

async def get_query_ratio(info, aggregate_filter, count, full_query):
    filtered_len = await count(info, aggregate_filter)
    total_len = await count(info, full_query)

    return total_len if total_len == 0 else filtered_len / total_len