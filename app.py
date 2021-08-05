from api.query import Query
from starlette.responses import Response
from starlette.websockets import WebSocket
import strawberry
from api.schemas.phenopacket import get_phenopackets
from typing import Optional, Union, Any
from strawberry.asgi import GraphQL as BaseGraphQL
from strawberry.dataloader import DataLoader
from starlette.requests import Request
from api.schema import schema
from fastapi import FastAPI
class MyGraphQL(BaseGraphQL):
    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ):
        return {"request": request, "response": response, "phenopacket_loader": DataLoader(load_fn=get_phenopackets)}

schema = strawberry.Schema(query=Query)
graphql_app = MyGraphQL(schema)
app = FastAPI()
app.add_route("/graphql", graphql_app)