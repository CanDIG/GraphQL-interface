from api.schemas.utils import generic_resolver
from typing import List, Optional
import strawberry
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket, PhenopacketInputType

@strawberry.type
class PhenopacketDataModels:
    @strawberry.field
    async def phenopackets(self, info, input: Optional[PhenopacketInputType] = None) -> List[Phenopacket]:
        return await generic_resolver(info, "phenopackets_loader", input, Phenopacket)