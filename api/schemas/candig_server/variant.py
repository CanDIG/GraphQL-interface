from pprint import pprint
from api.schemas.katsu.phenopacket.individual import Individual, IndividualInputType
from api.schemas.dataloader_input import DataLoaderInput
from api.schemas.utils import get_candig_server_response, get_post_search_body, get_post_variant_search_body, get_token, post_candig_server_response
from typing import List, Optional
import strawberry
from api.schemas.scalars.json_scalar import JSONScalar
from graphql import GraphQLError

"""
CanDIG server variants dataloader function

NOTE: 
    There are a couple of sections of the code below that take the form `if len(res_variants) == 0 and got_error ...`. These sections,
    exist to inform the client that no database within the CanDIG Server has a variant of the specified type. In these cases, we would have the
    variant array length being zero (len(res_variants) == 0) and got_error == True since the CanDIG server returns a 404 Error if it doesn't find a 
    response. We then raise an error of our own to inform the GraphQL client and any callers to this function that no variants were found. 

    Without this try-except and len(res_variant) checking, the function would error out if the first database didn't contain the specified variant,
    even if later ones did. Catching the errors during searches and instead only raising an error if all the searches turn up empty ensures that
    all databases are searched. 
"""
async def get_candig_server_variants(param):
    datasets_response = post_candig_server_response("datasets/search")
    got_error = False
    ret = []
    for dataloader_input in param:
        if dataloader_input.dataset_ids != None:
            res_variants = []
            for dataset_id in dataloader_input.dataset_ids:
                body = get_post_search_body(input = dataloader_input.input, dataset_id = dataset_id, patient_id = dataloader_input.patient_id)
                try:
                    results = post_candig_server_response("search", body)["results"]["variants"]
                except:
                    got_error = True
                    continue

                res_variants.extend([CandigServerVariant(**v) for v in results])
            
            if len(res_variants) == 0 and got_error: 
                raise GraphQLError("Error response from Candig Server!")

            ret.append(res_variants)
        else:
            res_variants = []
            for dataset in datasets_response["results"]["datasets"]:
                if dataloader_input.patient_id == None:
                    try:
                        results = post_candig_server_response("variants/search", body=get_post_variant_search_body(dataset["id"], dataloader_input.input))["results"]["variants"]
                    except:
                        got_error = True
                        continue

                    res_variants.extend([CandigServerVariant(**v) for v in results])
                else:
                    body = get_post_search_body(input = dataloader_input.input, dataset_id = dataset["id"], patient_id = dataloader_input.patient_id)
                    try:
                        results = post_candig_server_response("search", body)["results"]["variants"]
                    except:
                        got_error = True
                        continue

                    res_variants.extend([CandigServerVariant(**v) for v in results])
            
            if len(res_variants) == 0 and got_error: 
                raise GraphQLError("Error response from Candig Server!")
            
            ret.append(res_variants)
    return ret


@strawberry.input
class CandigServerVariantInput:
    start: Optional[str] = None
    end: Optional[str] = None
    referenceName: Optional[str] = None
    katsu_individual: Optional[IndividualInputType] = None

    def __eq__(self, o: object) -> bool:
        return self.start == o.start and self.end == o.end and self.referenceName == o.referenceName


@strawberry.type
class CandigServerVariant:
    id: Optional[strawberry.ID] = None
    variantSetId: Optional[strawberry.ID] = None
    names: Optional[List[str]] = None
    referenceName: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    referenceBases: Optional[str] = None
    alternateBases: Optional[List[str]] = None
    filtersApplied: Optional[bool] = None
    filtersPassed: Optional[bool] = None
    attributes: Optional[JSONScalar] = None

    @strawberry.field
    async def get_katsu_individuals(self, info) -> Optional[Individual]:
        token = get_token(info)
        patient_id = self.get_patient_id()
        res = await info.context["individuals_loader"].load(DataLoaderInput(token, [patient_id]))
        ind = None
        for x in res.output:
            if x["id"] == patient_id:
                ind = x
        if ind != None:
            return Individual.deserialize(ind)
        return None

    def get_patient_id(self):
        variant_set = get_candig_server_response(f"variantsets/{self.variantSetId}")
        return variant_set["results"]["patientId"]

class CandigServerVariantDataLoaderInput:
    def __init__(self, dataset_ids, input: CandigServerVariantInput, patient_id):
        self.dataset_ids = dataset_ids
        self.input = input
        self.patient_id = patient_id

    def __hash__(self):
        return hash((self.dataset_ids, self.input.start, self.input.end, self.input.referenceName, self.patient_id))

    def __eq__(self, o: object) -> bool:
        return self.dataset_ids == o.dataset_ids and self.input == o.input and self.patient_id == o.patient_id
