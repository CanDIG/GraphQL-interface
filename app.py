from typing import Union, Any
from strawberry.asgi import GraphQL, WebSocketHandler
from strawberry.dataloader import DataLoader

from starlette.requests import Request
from api.schema import schema
# from api.schemas.phenopacket import get_phenopackets

class MyGraphQL(GraphQL):
    async def get_context(self, request: Union[Request, WebSocketHandler]) -> Any:
        return {
            # "phenopacket_loader": DataLoader(load_fn=get_phenopackets)
        }


app = MyGraphQL(schema)