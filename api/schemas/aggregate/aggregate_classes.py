from api.schemas.katsu.phenopacket.phenopacket import Phenopacket, PhenopacketInputType
from api.schemas.candig_server.variant import CandigServerVariantInput
from api.schemas.beacon.beacon_data_models import BeaconAlleleRequest
from api.schemas.katsu.mcode.mcode_packet import MCodePacketInputType
from api.interfaces.input import Input
from typing import List, Optional
from dataclasses import field
import strawberry

@strawberry.input
class AggregateQueryFilter(Input):
    phenopacket_filter: Optional[PhenopacketInputType] = None
    mcodepacket_filter: Optional[MCodePacketInputType] = None
    variant_filter: Optional[CandigServerVariantInput] = None
    # beacon_filter: Optional[BeaconAlleleRequest] = None 
        # TODO: Add Features related to this when we fully integrate v2 spec

@strawberry.input
class IndividualQueryColumns(Input):
    column_names: Optional[List[str]] = None

# TODO: Add other nested object fields as query columns
#       Now we only have subject
@strawberry.input
class PhenopacketQueryColumns(Input):
    column_names: Optional[List[str]] = field(default_factory=list)
    subject: Optional[IndividualQueryColumns] = None
    phenotypic_features: Optional[IndividualQueryColumns] = None
    biosamples: Optional[IndividualQueryColumns] = None


@strawberry.input
class AggregateQueryColumns(Input):
    phenopacket: Optional[PhenopacketQueryColumns] = None