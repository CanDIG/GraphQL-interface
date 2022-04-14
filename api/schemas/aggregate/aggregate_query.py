from api.schemas.aggregate.ratio import get_phenopacket_ratio, get_mcodepacket_ratio, get_variants_ratio
from api.schemas.aggregate.count import count_phenopackets, count_mcodepackets, count_variants
from api.schemas.aggregate.aggregate_classes import AggregateQueryFilter
from api.schemas.aggregate.machine_learning import MachineLearningQuery
import strawberry

@strawberry.type
class AggregateQuery:
    @strawberry.field
    async def machine_learning(self, info) -> MachineLearningQuery:
        return MachineLearningQuery()
    
    @strawberry.field
    async def count(self, info, aggregate_filter: AggregateQueryFilter = None) -> int:
        if aggregate_filter.phenopacket_filter != None:
            return await count_phenopackets(info, aggregate_filter.phenopacket_filter)
        elif aggregate_filter.mcodepacket_filter != None:
            return await count_mcodepackets(info, aggregate_filter.mcodepacket_filter)
        elif aggregate_filter.variant_filter != None:
            return await count_variants(info, aggregate_filter.variant_filter)
            
        return 0

    @strawberry.field
    async def ratio(self, info, aggregate_filter: AggregateQueryFilter = None) -> float:
        if aggregate_filter.phenopacket_filter != None:
            return await get_phenopacket_ratio(info, aggregate_filter, self.count)
        elif aggregate_filter.mcodepacket_filter != None:
            return await get_mcodepacket_ratio(info, aggregate_filter, self.count)
        elif aggregate_filter.variant_filter != None:
            return await get_variants_ratio(info, aggregate_filter, self.count)

        return 0.0