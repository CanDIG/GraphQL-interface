from api.schemas.candig_server.variant import CandigServerVariantInput, \
    CandigServerVariantDataLoaderInput, get_candig_server_variants, CandigServerVariant
from typing import List, Optional, Tuple, Union
from api.schemas.katsu.mcode.mcode_packet import MCodePacket
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket
from api.schemas.utils import generic_resolver
from api.schemas.katsu.phenopacket.individual import Individual
from api.settings import GRAPHQL_BEACON_ID, GRAPHQL_BEACON_VERSION
from strawberry.dataloader import DataLoader
import strawberry


'''
BeaconAlleleDataLoaderInput:
    Description:
        Simple Class that is used in the DataLoader functions to process requests for Beacon V1 in batches.

    Fields:
        input: a BeaconAlleleRequest Object containing a specific user query
        info: a ContextInfo Object containing meta information about the query like headers
'''
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


'''
BeaconAlleleRequest:
    Description:
        An input type of the strawberry module, used to read in the user's requirements for the 
        allele's they wish to search for. 

    Fields:
        Listed Below.
'''
beacon_allele_request_description = '''
Beacon V1 Field: Input to be specified to query the Beacon endpoint.
'''
beacon_ref_name = '''
Beacon V1 Field: The name of the chromosome in which the variant is located.
'''
beacon_ref_base = '''
Beacon V1 Field: The reference base of the variant in question.
'''
beacon_alt_base = '''
Beacon V1 Field: An Alternate base of the variant in question.
'''
beacon_start_pos = '''
Beacon V1 Field: Start coordinate of the range in which to search for the variant.
'''
beacon_end_pos = '''
Beacon V1 Field: End coordinate of the range in which to search for the variant.
'''
beacon_dataset = '''
CanDIG Server Field: IDs of the CanDIG Datasets in which to search for the variants.
'''
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
    
    def __hash__(self) -> int:
        return hash((
            self.referenceName, self.referenceBases, self.start, self.end, self.alternateBases, self.datasetIds
        ))


'''
BeaconReturnableRequest:
    Description: 
        A strawberry type object holding the same fields as the BeaconAlleleRequest, but simply used for returning the
        original request object in the BeaconAlleleResponse. This is done to accomodate the BeaconV1 specification which 
        requires returning a copy of the original request to the user, even though strawberry.input classes cannot be
        returned to the user through GraphQL.
    
    Fields: 
        Same as BeaconAlleleRequest.
'''
beacon_returnable_req_description = '''
Beacon V1 Field: Description of Original Request to Beacon GraphQL endpoint.
'''
@strawberry.type(description=beacon_returnable_req_description)
class BeaconReturnableRequest:
    referenceName: str = strawberry.field(description=beacon_ref_name)
    referenceBases: str = strawberry.field(description=beacon_ref_base)
    start: int = strawberry.field(description=beacon_start_pos)
    end: int = strawberry.field(description=beacon_end_pos)
    alternateBases: str = strawberry.field(description=beacon_alt_base)
    datasetIds: Optional[List[str]] = strawberry.field(default=None, description=beacon_dataset)


'''
BeaconError: 
    Description:
        A strawberry type object used to return an error code and error message in the event of an error
        during the BeaconQuery. 
    
    Fields:
        Listed Below.
'''
beacon_error_description = '''
Beacon V1 Field: Error Code and Message populated in the event of a failed request to the 
Beacon endpoint.
'''
beacon_error_code = '''
Beacon V1 Field: Error Code received if request did not go through.
'''
beacon_error_message = '''
Beacon V1 Field: Error Message received if request did not go through.
'''
@strawberry.type(description=beacon_error_description)
class BeaconError:
    errorCode: Optional[int] = strawberry.field(default=None, description=beacon_error_code)
    errorMessage: Optional[str] = strawberry.field(default=None, description=beacon_error_message)


'''
BeaconIndividual:
    Description:
        A strwberry type object used to return personal and clinical information on patients located within
        the Katsu Database carrying a variant of the type requested.
    
    Fields:
        Listed Below.
'''
beacon_individual_description = '''
Beacon V2 Extension Field: Personal Information & Clinical Data for any patients in the Katsu Database 
that carry a variant of the type requested.
'''
beacon_personal_info = '''
Beacon V2 Extension: Provides personal information on patients with variants in the specified range.
'''
beacon_mcode = '''
Beacon V2 Extension: Provides clinical mCODE information on patients with variants in the specified range.
'''
beacon_phenopacket = '''
Beacon V2 Extension: Provides phenopacket information on patients with variants in the specified range.
'''
@strawberry.type(description=beacon_individual_description)
class BeaconIndividual:
    personalInfo: Optional[Individual] = strawberry.field(default=None, description=beacon_personal_info)
    mcodepackets: Optional[MCodePacket] = strawberry.field(default=None, description=beacon_mcode)
    phenopackets: Optional[Phenopacket] = strawberry.field(default=None, description=beacon_phenopacket)


'''
BeaconAlleleResponse:
    Description:
        A strawberry type object used to return a response to the user after their request to the
        GraphQL beacon endpoint. 
    
    Fields:
        Listed Below.
    
    NOTE:
        beaconId: Documents the provider of the API and is a required specification in Beacon V1. Is the same for all queries.
        api_version: Documents the version of the Beacon API used and is a required Beacon V1 spec. It is the same for all queries.
'''
beacon_allele_response_description = '''
Beacon V1 Field: Response received from a Beacon Query. Beacon V1 specifications are enabled, 
alongside additional clinical data in preparation for Beacon V2.
'''
beacon_exists_description = '''
Beacon V1 Field: Specifies whether the specified variant had patients available in the Katsu database.
'''
beacon_id_description = '''
Beacon V1 Field: Identifies the provider of the Beacon API.
'''
beacon_api_version_description = '''
Beacon V1 Field: Identifies the version of the Beacon API that is in use.
'''
beacon_individuals_present_description = '''
Beacon V2 Extension: Provides clinical and personal information for Variants within the specified range with patients in Katsu.
'''
@strawberry.type(description=beacon_allele_response_description)
class BeaconAlleleResponse:
    exists: Optional[bool] = strawberry.field(default=None, description=beacon_exists_description)
    error: Optional[BeaconError] = strawberry.field(default=None, description=beacon_error_description)
    alleleRequest: Optional[BeaconReturnableRequest] = strawberry.field(default=None, description=beacon_returnable_req_description)

    @strawberry.field(description=beacon_id_description)
    def beaconId(self) -> str:
        return GRAPHQL_BEACON_ID
    
    @strawberry.field(description=beacon_api_version_description)
    def apiVersion(self) -> str:
        return GRAPHQL_BEACON_VERSION

    @strawberry.field(description=beacon_individuals_present_description)
    async def individuals_present(self, info) -> List[BeaconIndividual]:
        if self.exists is False: 
            print('individuals_present: BeaconAlleleResponse: beacon_data_models.py - Cannot find individuals for variant that doesn\'t exist in Katsu')
            return []
        
        return await self.get_individuals(info)
    
    ''' get_variants(info): Return CandigServerVariants matching input specs'''
    async def get_variants(self, info) -> List[CandigServerVariant]:
        start, end, name, _, _, datasets = self.get_request_info()
        variant_in = CandigServerVariantInput(start=start, end=end, referenceName=name)
        loader_in = CandigServerVariantDataLoaderInput(datasets, variant_in, None, info)

        try: 
            return await DataLoader(load_fn=get_candig_server_variants).load(loader_in)
        except Exception as e:
            print(f'get_variants: BeaconAlleleResponse: beacon_data_models.py - Error in finding variants from CanDIG - \n \tError: {e}')
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
        variants = await self.get_variants(info)

        for variant in variants:
            if variant_matches(variant, str(start), str(end), name, base, alt_base):
                try:
                    individual = await variant.get_katsu_individuals(info)
                    matching_mcode = self.find_packet(all_mcode_data, individual.id)
                    matching_phenopacket = self.find_packet(all_phenotype_data, individual.id)
                    individuals_list.append(BeaconIndividual(individual, matching_mcode, matching_phenopacket))
                except Exception as e:
                    print(f'get_individuals: BeaconAlleleResponse: beacon_data_models.py - Error in getting patients with the specified variant - \n \tError: {e}')
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


''' get_beacon_alleles(param): Beacon V1 DataLoader function to get BeaconAlleleResponse objects from requests, in batches'''
async def get_beacon_alleles(param):
    to_return = []
    for input in param:
        base_allele_request = get_request(input.input)
        start, end, name, base, alt_base, datasets = collect_input_fields(input.input)
        variant_in = CandigServerVariantInput(start=start, end=end, referenceName=name)
        loader_in = CandigServerVariantDataLoaderInput(datasets, variant_in, None, input.info)
        
        try: 
            variants = await DataLoader(load_fn=get_candig_server_variants).load(loader_in)
            have_individuals = await individuals_present(variants, start, end, name, base, alt_base, input.info)
            to_return.append(build_response(have_individuals, base_allele_request))
        except Exception as e:
            if f'{e}' == 'NON-200 response from Candig Server!':
                print(f'get_beacon_alleles: beacon_data_models.py - No patient exists with specified variant:\n--- \
                \nStart: {start} \nEnd: {end} \nReference Name: {name} \nReference Base: {base} \nAlternate Base: {alt_base}\n---')
                to_return.append(build_response(False, base_allele_request, None))
            else:
                print(f'get_beacon_alleles: beacon_data_models.py - Error in finding patients with specified variant - \n \tError: {e}')
                to_return.append(build_response(None, base_allele_request, BeaconError(errorCode=404, errorMessage=f'{e}')))
        
    return to_return


'''collect_input_fields(input): Collect cleaned input data from user request'''
def collect_input_fields(input: BeaconAlleleRequest) -> Tuple[str, str, str, str, str, Optional[List[str]]]:
    return str(input.start), str(input.end), input.referenceName, input.referenceBases, input.alternateBases, input.datasetIds


''' variant_matches(variant, start, end, name, base, alt_base): Check if the variant matches given input fields'''
def variant_matches(variant: CandigServerVariant, start: str, end: str, name: str, base: str, alt_base: str) -> bool:
    return variant.referenceName == name and variant.start >= start and variant.end <= end and \
        alt_base in variant.alternateBases and variant.referenceBases == base


''' build_response(exists, request): Return a BeaconAlleleResponse object from given fields'''
def build_response(exists: Optional[bool] = None, request: Optional[BeaconReturnableRequest] = None, error: Optional[BeaconError] = None) -> BeaconAlleleResponse:
    return BeaconAlleleResponse(exists=exists, alleleRequest=request, error=error)


''' get_request(input): Convert a BeaconAlleleRequest input object to returnable BeaconReturnableRequest type. 
        NOTE: This function is required since the strawberry GraphQL service cannot return strawberry.input objects,
        which our original BeaconAlleleRequest objects are, and can only return strawberry.type objects, like the
        BeaconReturnableRequest object. This function thus converts all of the fields in the input object to a returnable form.
'''
def get_request(input: BeaconAlleleRequest) -> BeaconReturnableRequest:
    return BeaconReturnableRequest(
        referenceName=input.referenceName, referenceBases=input.referenceBases, 
        alternateBases=input.alternateBases, start=input.start, end=input.end, datasetIds=input.datasetIds
    )


''' get_individuals(variants, start, end, name, base, alt_base, info): Check if there are individuals
        whose records match the input categories'''
async def individuals_present(variants: List[CandigServerVariant], start: str, end: str, name: str, base: str, alt_base: str, info) -> bool:
    for variant in variants:
        try:
            if variant_matches(variant, start, end, name, base, alt_base):
                if await variant.get_katsu_individuals(info) is not None:
                    return True 
        except Exception:
            pass
    
    print(f'---\n No patient exists with specified variant: \nStart: {start} \nEnd: {end} \nReference Name: {name} \nReference Base: {base} \nAlternate Base: {alt_base}\n---')
    return False