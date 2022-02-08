from typing import List, Optional, Tuple, Union
from api.schemas.katsu.mcode.mcode_packet import MCodePacket
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket
from api.schemas.utils import generic_resolver
import strawberry
from api.schemas.candig_server.variant import CandigServerVariantInput, \
    CandigServerVariantDataLoaderInput, get_candig_server_variants, CandigServerVariant
from strawberry.dataloader import DataLoader
from api.schemas.katsu.phenopacket.individual import Individual
from api.schemas.beacon.beacon_descriptions import *

''' 
    get_beacon_alleles(param): Beacon V1 DataLoader function -> Passed in a List
        of BeaconAlleleDataLoaderInput objects, param, and returns a List of 
        BeaconAlleleResponse objects, one for each of the requests sent in
'''
async def get_beacon_alleles(param):
    to_return = []
    for input in param:
        base_allele_request=get_beacon_request(input.input)
        
        if is_missing_required_params(input.input):
            to_return.append(generate_missing_response(base_allele_request))
            continue

        start, end, reference_name, reference_base, alternate_base, datasets = collect_input_fields(input.input)
        variant_in = CandigServerVariantInput(start=start, end=end, referenceName=reference_name)
        loader_in = CandigServerVariantDataLoaderInput(datasets, variant_in, None)
        
        try:
            variants = await DataLoader(load_fn=get_candig_server_variants).load(loader_in)
        except:
            to_return.append(build_response(False, base_allele_request))
            continue

        individuals_list = await get_individuals(variants, start, end, reference_name, reference_base, alternate_base, input.info)
        if len(individuals_list) > 0:
            to_return.append(build_response(True, base_allele_request, individuals_list))
        else:
            to_return.append(build_response(False, base_allele_request))
        
    return to_return

@strawberry.input(description=beacon_allele_request_description)
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

@strawberry.type(description=beacon_error_description)
class BeaconError:
    errorCode: Optional[int] = None
    errorMessage: Optional[str] = None

@strawberry.type(description=beacon_og_request_description)
class BeaconOriginalRequest:
    referenceName: str
    referenceBases: str
    start: int
    end: int
    alternateBases: Optional[str] = None
    variantType: Optional[str] = None
    datasetIds: Optional[List[str]] = None

@strawberry.type(description=beacon_individual_description)
class BeaconIndividual:
    personalInfo: Optional[Individual] = None
    mcodepackets: Optional[MCodePacket] = None
    phenopackets: Optional[Phenopacket] = None

@strawberry.type(description=beacon_allele_response_description)
class BeaconAlleleResponse:
    exists: Optional[bool] = None
    error: Optional[BeaconError] = None
    alleleRequest: Optional[BeaconOriginalRequest] = None
    individualsPresent: Optional[List[BeaconIndividual]] = None

    @strawberry.field
    def beaconId(self, info) -> str:
        return 'com.distributedgenomics'
    
    @strawberry.field
    def apiVersion(self, info) -> str:
        return '1.0.0'

class BeaconAlleleDataLoaderInput:
    def __init__(self, input, info) -> None:
        self.input = input
        self.info = info
    
    def __eq__(self, o: object) -> bool:
        return isinstance(o, BeaconAlleleDataLoaderInput) and self.input == o.input
    
    def __hash__(self) -> int:
        return hash((
            self.input.referenceName, self.input.referenceBases, self.input.start, self.input.end,
            self.input.alternateBases, self.input.variantType
        ))

'''
    is_missing_required_params(input): Passed in a BeaconAlleleRequest object, 
        request, this function returns a boolean as to whether the alternateBases 
        and variantType fields are both null, since at least one has to be non-null
'''
def is_missing_required_params(input: BeaconAlleleRequest) -> bool:
    return input.alternateBases is None and input.variantType is None

'''
    collect_input_fields(input): Passed in a BeaconAlleleRequest object, request, 
        this function returns a Tuple containing the input fields collected such 
        as the start, end coordinates of the Allele, etc.
'''
def collect_input_fields(input: BeaconAlleleRequest) -> Tuple[str, str, str, str, str, Optional[List[str]]]:
    start = str(input.start) if input.start else "0"
    end = str(input.end) if input.end else "0"
    rName = input.referenceName
    rBase = input.referenceBases
    aBase = input.alternateBases
    dSets = input.datasetIds

    referenceName = rName if rName else "1"
    referenceBase = rBase if rBase else "A"
    alternateBase = aBase if aBase else "A"
    datasets = dSets if dSets else None

    return start, end, referenceName, referenceBase, alternateBase, datasets

'''
    variant_matches(variant, start, end, name, r_base, a_base): Passed in a CandigServerVariant 
        object, variant, and returns a bool as to whether variant's fields match the passed in 
        characteristics start, end, name, r_name, r_base and a_base 
'''
def variant_matches(variant: CandigServerVariant, start: str, end: str, name: str, r_base: str, a_base: str) -> bool:
    v_start = variant.start
    v_end = variant.end
    v_rname = variant.referenceName
    v_rbase = variant.referenceBases
    v_abase = variant.alternateBases

    return v_rname == name and v_start >= start and v_end <= end and a_base in v_abase and r_base == v_rbase

''''
    build_response(exists, request, people): Passed in a bool, exists, a BeaconOriginalRequest
        object request and an Optional list of Individuals and returns a BeaconAlleleResponse 
        object encapsulating these values
'''
def build_response(exists: bool, request: BeaconOriginalRequest, people: Optional[List[BeaconIndividual]] = None) -> BeaconAlleleResponse:
    return BeaconAlleleResponse(exists=exists, alleleRequest=request, individualsPresent=people)

'''
    binary_search_packets(packets, patient_id, start, end): Recursive function that takes
        in a sorted list of either mCODE packets or phenopackets and returns an optional 
        response that is either an mCODE packet of a phenopacket matching the patient_id
'''
def binary_search_packets(packets: Union[List[MCodePacket], List[Phenopacket]], patient_id: str, start: int, end: int):
    if end < start: return None
    
    mid_index = (start + end) // 2
    middle = packets[mid_index]
    middle_id = middle.subject.id

    if middle_id == patient_id: return middle
    elif middle_id < patient_id: return binary_search_packets(packets, patient_id, mid_index + 1, end)
    elif middle_id > patient_id: return binary_search_packets(packets, patient_id, start, mid_index - 1)

'''
    find_packet(packets, patient_id): Passed in either a list of mCODE packets or a list
        phenopackets as well as a string for the patient_id and returns an optional
        response that is either an mCODE packet or phenopacket, depending on the type passed
        in
'''
def find_packet(packets: Union[List[MCodePacket], List[Phenopacket]], patient_id: str) -> Optional[Union[MCodePacket, Phenopacket]]:
    packets = sorted(packets, key=lambda packet: packet.subject.id)
    return binary_search_packets(packets, patient_id, 0, len(packets) - 1)

'''
    get_individuals(variants, start, end, r_name, r_base, a_name, info): Passed in a 
        list of CandigServerVariants and returns a list of Individuals whose records 
        match the start, ed, r_name, r_base and a_base characteristics passed in
'''
async def get_individuals(variants: List[CandigServerVariant], start: str, end: str, r_name: str, r_base: str, a_base: str, info) -> List[BeaconIndividual]:
    individuals_list = []
    all_mcode_data = await generic_resolver(info, "mcode_packets_loader", None, MCodePacket)
    all_phenotype_data = await generic_resolver(info, "phenopackets_loader", None, Phenopacket)

    for variant in variants:
        if variant_matches(variant, start, end, r_name, r_base, a_base):
            try:
                individual = await variant.get_katsu_individuals(info)
                matching_mcode = find_packet(all_mcode_data, individual.id)
                matching_phenopacket = find_packet(all_phenotype_data, individual.id)
                individuals_list.append(BeaconIndividual(individual, matching_mcode, matching_phenopacket))
            except:
                pass
    
    return individuals_list

''' 
    get_beacon_request(input): Passed in a BeaconAlleleRequest Object, input, 
        this function returns a BeaconOriginalRequest Object with the same 
        fields as the original request object. This is because the original 
        BeaconAlleleRequest object is a strawberry.input type and cannot be
        returned
'''
def get_beacon_request(input: BeaconAlleleRequest) -> BeaconOriginalRequest:
    return BeaconOriginalRequest(
        referenceName=input.referenceName, referenceBases=input.referenceBases,
        alternateBases=input.alternateBases, start=input.start, end=input.end,
        datasetIds=input.datasetIds, variantType=input.variantType
    )

'''
    generate_missing_response(base_allele_request): Passed in a BeaconOriginalRequest
        object, request, the function returns a BeaconAlleleRequest object with an error 
        message detailing the missing fields
'''
def generate_missing_response(base_allele_request: BeaconOriginalRequest) -> BeaconAlleleResponse:
    error_message = 'One of variantType or alternateBases must be specified'
    return BeaconAlleleResponse(alleleRequest=base_allele_request, error=BeaconError(400, error_message))