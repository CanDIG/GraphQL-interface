from api.schemas.utils import generic_load_fn
from api.schemas.candig_server.variant import get_candig_server_variants
from api.schemas.beacon.beacon_data_models import get_beacon_alleles
from api.query import Query
from starlette.responses import Response
from starlette.websockets import WebSocket
import strawberry
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket
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
        return {"request": request, 
                "response": response, 
                "phenopackets_loader": DataLoader(load_fn=generic_load_fn("phenopackets")), 
                "individuals_loader": DataLoader(load_fn=generic_load_fn("individuals")),
                # mcode data loaders
                "mcode_packets_loader": DataLoader(load_fn=generic_load_fn("mcodepackets")),
                "mcode_genetic_specimens_loader": DataLoader(load_fn=generic_load_fn("geneticspecimens")),
                "mcode_genomic_regions_studied_loader": DataLoader(load_fn=generic_load_fn("genomicregionsstudied")),
                "mcode_genomics_reports_loader": DataLoader(load_fn=generic_load_fn("genomicsreports")),
                "mcode_labs_vital_loader": DataLoader(load_fn=generic_load_fn("labsvital")),
                "mcode_cancer_conditions_loader": DataLoader(load_fn=generic_load_fn("cancerconditions")),
                "mcode_tnm_staging_loader": DataLoader(load_fn=generic_load_fn("tnmstaging")),
                "mcode_cancer_related_procedures_packets_loader": DataLoader(load_fn=generic_load_fn("cancerrelatedprocedures")),
                "mcode_medication_statements_packets_loader": DataLoader(load_fn=generic_load_fn("medicationstatements")),
                "candig_server_variants_loader": DataLoader(load_fn=get_candig_server_variants),
                "beacon_allele_response_loader": DataLoader(load_fn=get_beacon_alleles)
                }

schema = strawberry.Schema(query=Query)
graphql_app = MyGraphQL(schema)
app = FastAPI()
app.add_route("/", graphql_app)