from api.query import Query
import strawberry

schema = strawberry.Schema(query = Query)