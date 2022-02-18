from typing import List, Optional
import strawberry


''' 
    get_beacon_request(input): Passed in a BeaconAlleleRequest Object, input, 
        this function returns a BeaconOriginalRequest Object with the same 
        fields as the original request object. This is because the original 
        BeaconAlleleRequest object is a strawberry.input type and cannot be
        returned
'''
def get_beacon_request(input):
    return BeaconOriginalRequest(
        referenceName=input.referenceName, referenceBases=input.referenceBases,
        alternateBases=input.alternateBases, start=input.start, end=input.end,
        datasetIds=input.datasetIds, variantType=input.variantType
    )


''' 
    get_beacon_alleles(param): Beacon V1 DataLoader function -> Passed in a List
        of BeaconAlleleDataLoaderInput objects, param, and returns a List of 
        BeaconAlleleResponse objects, one for each of the requests sent in
'''
async def get_beacon_alleles(param):
    ret = []
    for input in param:
        ret.append(
            BeaconAlleleResponse(
                exists=True, alleleRequest=get_beacon_request(input.input)
            )
        )
    return ret


@strawberry.input
class BeaconAlleleRequest:
    referenceName: str
    referenceBases: str
    start: int
    end: int
    alternateBases: Optional[str] = None
    variantType: Optional[str] = None
    datasetIds: Optional[List[str]] = None

    def __eq__(self, o: object) -> bool:
        return isinstance(o, BeaconAlleleRequest) and self.referenceName == o.referenceName \
            and self.referenceBases == o.referenceBases and self.start == o.start and self.end == o.end \
            and self.alternateBases == o.alternateBases and self.variantType == o.variantType \
            and self.datasetIds == o.datasetIds


@strawberry.type
class BeaconError:
    errorCode: Optional[int] = None
    errorMessage: Optional[str] = None


@strawberry.type
class BeaconOriginalRequest:
    referenceName: str
    referenceBases: str
    start: int
    end: int
    alternateBases: Optional[str] = None
    variantType: Optional[str] = None
    datasetIds: Optional[List[str]] = None


@strawberry.type
class BeaconAlleleResponse:
    exists: Optional[bool] = None
    error: Optional[BeaconError] = None
    alleleRequest: Optional[BeaconOriginalRequest] = None

    @strawberry.field
    def beaconId(self, info) -> str:
        return 'com.distributedgenomics'
    
    @strawberry.field
    def apiVersion(self, info) -> str:
        return '1.0.0'


class BeaconAlleleDataLoaderInput:
    def __init__(self, input) -> None:
        self.input = input
    
    def __eq__(self, o: object) -> bool:
        return isinstance(o, BeaconAlleleDataLoaderInput) and self.input == o.input
    
    def __hash__(self) -> int:
        return hash((
            self.input.referenceName, self.input.referenceBases, self.input.start, self.input.end,
            self.input.alternateBases, self.input.variantType
        ))
