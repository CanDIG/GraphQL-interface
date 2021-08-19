from pprint import pprint
from api.schemas.individual import Individual, IndividualInputType
from api.schemas.dataloader_input import DataLoaderInput
from api.schemas.utils import get_candig_server_response, get_post_search_body, get_post_variant_search_body, get_token, post_candig_server_response
from typing import List, Optional
import strawberry
"""
CanDIG server variants dataloader function
"""
async def get_candig_server_variants(param):
    datasets_response = post_candig_server_response("datasets/search")
    ret = []
    for dataloader_input in param:
        if dataloader_input.dataset_ids != None:
            res_variants = []
            for dataset_id in dataloader_input.dataset_ids :
                body = get_post_search_body(input = dataloader_input.input, dataset_id = dataset_id, patient_id = dataloader_input.patient_id)
                results = post_candig_server_response("search", body)["results"]["variants"]
                res_variants.extend([CandigServerVariant(**v) for v in results])
            ret.append(res_variants)
        else:
            res_variants = []
            for dataset in datasets_response["results"]["datasets"]:
                if dataloader_input.patient_id == None:
                    results = post_candig_server_response("variants/search", body=get_post_variant_search_body(dataset["id"], dataloader_input.input))["results"]["variants"]
                    res_variants.extend([CandigServerVariant(**v) for v in results])
                else:
                    body = get_post_search_body(input = dataloader_input.input, dataset_id = dataset["id"], patient_id = dataloader_input.patient_id)
                    results = post_candig_server_response("search", body)["results"]["variants"]
                    res_variants.extend([CandigServerVariant(**v) for v in results])
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
    referenceName: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    referenceBases: Optional[str] = None
    alternateBases: Optional[List[str]] = None
    filtersApplied: Optional[bool] = None
    filtersPassed: Optional[bool] = None

    @strawberry.field
    async def get_katsu_individuals(self, info) -> List[Individual]:
        token = get_token(info)
        patient_id = self.get_patient_id()
        print(patient_id)
        res = await info.context["individual_loader"].load(DataLoaderInput(token, patient_id))
        return res.output

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