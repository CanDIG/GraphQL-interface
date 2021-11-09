from api.schemas.katsu.mcode.mcode_data_models import McodeDataModels
from api.schemas.katsu.mcode.mcode_packet import MCodePacket
from typing import Optional
from api.schemas.katsu.phenopacket.phenopacket_data_models import PhenopacketDataModels
import strawberry

@strawberry.type
class KatsuDataModels:
    @strawberry.field
    async def phenopacket_data_models(self, info) -> PhenopacketDataModels:
        return PhenopacketDataModels()
    
    @strawberry.field
    async def mcode_data_models(self, info) -> McodeDataModels:
        return McodeDataModels()