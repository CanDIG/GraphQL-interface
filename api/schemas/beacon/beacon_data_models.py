from api.schemas.candig_server.variant import CandigServerVariantInput, \
    CandigServerVariantDataLoaderInput, get_candig_server_variants, CandigServerVariant
from typing import List, Optional, Tuple, Union
from api.schemas.katsu.mcode.mcode_packet import MCodePacket
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket
from api.schemas.utils import generic_resolver
from api.schemas.katsu.phenopacket.individual import Individual
from api.schemas.beacon.beacon_descriptions import *
from strawberry.dataloader import DataLoader
import strawberry

class BeaconAlleleDataLoaderInput:
    def __init__(self, input, info) -> None:
        self.input = input
        self.info = info
    
    def __eq__(self, o: object) -> bool:
        return isinstance(o, BeaconAlleleDataLoaderInput) and self.input == o.input
    
    def __hash__(self) -> int:
        return hash((
            self.input.referenceName, self.input.referenceBases, self.input.start, self.input.end, self.input.alternateBases
        ))

@strawberry.input(description=beacon_allele_request_description)
class BeaconAlleleRequest:
    referenceName: str = strawberry.field(description=beacon_ref_name)
    referenceBases: str = strawberry.field(description=beacon_ref_base)
    start: int = strawberry.field(description=beacon_start_pos)
    end: int = strawberry.field(description=beacon_end_pos)
    alternateBases: str = strawberry.field(description=beacon_alt_base)
    datasetIds: Optional[List[str]] = strawberry.field(default=None, description=beacon_dataset)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, BeaconAlleleRequest) and self.referenceName == o.referenceName \
            and self.referenceBases == o.referenceBases and self.start == o.start and self.end == o.end \
            and self.alternateBases == o.alternateBases and self.datasetIds == o.datasetIds

@strawberry.type(description=beacon_og_request_description)
class BeaconOriginalRequest:
    referenceName: str = strawberry.field(description=beacon_ref_name)
    referenceBases: str = strawberry.field(description=beacon_ref_base)
    start: int = strawberry.field(description=beacon_start_pos)
    end: int = strawberry.field(description=beacon_end_pos)
    alternateBases: str = strawberry.field(description=beacon_alt_base)
    datasetIds: Optional[List[str]] = strawberry.field(default=None, description=beacon_dataset)

@strawberry.type(description=beacon_error_description)
class BeaconError:
    errorCode: Optional[int] = strawberry.field(default=None, description=beacon_error_code)
    errorMessage: Optional[str] = strawberry.field(default=None, description=beacon_error_message)

@strawberry.type(description=beacon_individual_description)
class BeaconIndividual:
    personalInfo: Optional[Individual] = strawberry.field(default=None, description=beacon_personal_info)
    mcodepackets: Optional[MCodePacket] = strawberry.field(default=None, description=beacon_mcode)
    phenopackets: Optional[Phenopacket] = strawberry.field(default=None, description=beacon_phenopacket)

@strawberry.type(description=beacon_allele_response_description)
class BeaconAlleleResponse:
    exists: Optional[bool] = strawberry.field(default=None, description=beacon_exists_description)
    error: Optional[BeaconError] = strawberry.field(default=None, description=beacon_error_description)
    alleleRequest: Optional[BeaconOriginalRequest] = strawberry.field(default=None, description=beacon_og_request_description)

    @strawberry.field(description=beacon_id_description)
    def beaconId(self) -> str:
        return 'com.candig.graphql-interface'
    
    @strawberry.field(description=beacon_api_version_description)
    def apiVersion(self) -> str:
        return '1.0.0'

    @strawberry.field(description=beacon_individuals_present_description)
    async def individuals_present(self, info) -> List[BeaconIndividual]:
        if self.exists is False: 
            return []
        
        return await self.get_individuals(info)
    
    ''' get_variants(): Return CandigServerVariants matching input specs'''
    async def get_variants(self) -> List[CandigServerVariant]:
        start, end, name, _, _, datasets = self.get_request_info()
        variant_in = CandigServerVariantInput(start=start, end=end, referenceName=name)
        loader_in = CandigServerVariantDataLoaderInput(datasets, variant_in, None)

        try: 
            return await DataLoader(load_fn=get_candig_server_variants).load(loader_in)
        except Exception:
            return []
    
    ''' get_request_info(): Get input specs requested by the user'''
    def get_request_info(self) -> Tuple[int, int, str, str, str, Optional[List[str]]]: 
        return self.alleleRequest.start, self.alleleRequest.end, self.alleleRequest.referenceName, \
            self.alleleRequest.referenceBases, self.alleleRequest.alternateBases, self.alleleRequest.datasetIds
    
    '''get_individuals(): Get BeaconIndividuals matching input specs'''
    async def get_individuals(self, info) -> List[BeaconIndividual]:
        individuals_list = []
        start, end, name, base, alt_base, _ = self.get_request_info()
        all_mcode_data = await generic_resolver(info, "mcode_packets_loader", None, MCodePacket) 
        all_phenotype_data = await generic_resolver(info, "phenopackets_loader", None, Phenopacket)
        variants = await self.get_variants()

        for variant in variants:
            if variant_matches(variant, str(start), str(end), name, base, alt_base):
                try:
                    individual = await variant.get_katsu_individuals(info)
                    matching_mcode = self.find_packet(all_mcode_data, individual.id)
                    matching_phenopacket = self.find_packet(all_phenotype_data, individual.id)
                    individuals_list.append(BeaconIndividual(individual, matching_mcode, matching_phenopacket))
                except:
                    pass
        
        return individuals_list
    
    ''' find_packet(packets, patient_id): Find mCODE/phenopacket that matches patient id'''
    def find_packet(self, packets: Union[List[MCodePacket], List[Phenopacket]], patient_id: str) -> Optional[Union[MCodePacket, Phenopacket]]:
        packets = sorted(packets, key=lambda packet: packet.subject.id)
        return self.binary_search_packets(packets, patient_id, 0, len(packets) - 1)
    
    ''' binary_search_packets(packets, patient_id, start, end): Search for packet with matching patient id'''
    def binary_search_packets(self, packets: Union[List[MCodePacket], List[Phenopacket]], patient_id: str, start: int, end: int) -> Optional[Union[MCodePacket, Phenopacket]]:
        if end < start: return None
        
        mid_index = (start + end) // 2
        middle = packets[mid_index]
        middle_id = middle.subject.id

        if middle_id == patient_id: return middle
        elif middle_id < patient_id: return self.binary_search_packets(packets, patient_id, mid_index + 1, end)
        elif middle_id > patient_id: return self.binary_search_packets(packets, patient_id, start, mid_index - 1)

''' get_beacon_alleles(param): Beacon V1 DataLoader function to get BeaconAlleleResponse objects from requests'''
async def get_beacon_alleles(param):
    to_return = []
    for input in param:
        base_allele_request = get_request(input.input)
        start, end, name, base, alt_base, datasets = collect_input_fields(input.input)
        variant_in = CandigServerVariantInput(start=start, end=end, referenceName=name)
        loader_in = CandigServerVariantDataLoaderInput(datasets, variant_in, None)
        
        try: 
            variants = await DataLoader(load_fn=get_candig_server_variants).load(loader_in)
            have_individuals = await individuals_present(variants, start, end, name, base, alt_base, input.info)
            to_return.append(build_response(have_individuals, base_allele_request))
        except Exception:
            to_return.append(build_response(False, base_allele_request))
        
    return to_return

'''collect_input_fields(input): Collect cleaned input data from user request'''
def collect_input_fields(input: BeaconAlleleRequest) -> Tuple[str, str, str, str, str, Optional[List[str]]]:
    return str(input.start), str(input.end), input.referenceName, input.referenceBases, input.alternateBases, input.datasetIds

''' variant_matches(variant, start, end, name, base, alt_base): Check if the variant matches given fields'''
def variant_matches(variant: CandigServerVariant, start: str, end: str, name: str, base: str, alt_base: str) -> bool:
    return variant.referenceName == name and variant.start >= start and variant.end <= end and \
        alt_base in variant.alternateBases and variant.referenceBases == base

''' build_response(exists, request): Return a BeaconAlleleResponse object from given fields'''
def build_response(exists: bool, request: Optional[BeaconOriginalRequest] = None) -> BeaconAlleleResponse:
    return BeaconAlleleResponse(exists=exists, alleleRequest=request)

''' get_request(input): Convert a BeaconAlleleRequest input object to returnable BeaconOriginalRequest type'''
def get_request(input: BeaconAlleleRequest) -> BeaconOriginalRequest:
    return BeaconOriginalRequest(
        referenceName=input.referenceName, referenceBases=input.referenceBases, 
        alternateBases=input.alternateBases, start=input.start, end=input.end, datasetIds=input.datasetIds
    )

''' get_individuals(variants, start, end, name, base, alt_base, info): Check if there are individuals
        whose records match the input categories'''
async def individuals_present(variants: List[CandigServerVariant], start: str, end: str, name: str, base: str, alt_base: str, info) -> bool:
    for variant in variants:
        try:
            if variant_matches(variant, start, end, name, base, alt_base):
                return True if await variant.get_katsu_individuals(info) is not None else False
        except Exception:
            pass
    
    return False