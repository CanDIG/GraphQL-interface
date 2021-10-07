from api.schemas.aggregate_query import AggregateQuery
from api.query import Query
import strawberry

schema = strawberry.Schema(query = Query)