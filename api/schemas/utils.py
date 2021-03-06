from api.interfaces.input import Input
import api.settings
import json
from api.schemas.dataloader_input import DataLoaderInput, DataLoaderOutput
from api.schemas.scalars.json_scalar import JSONScalar
import requests
from typing import List, NamedTuple
from graphql import GraphQLError

POST_SEARCH_BODY = {
    "datasetId": "-1",
    "logic": {
            "id": "A"
    },
    "components": [
        {
            "id": "A",
            "patients": {
                "filters": [
                    {
                        "field": "patientId",
                        "operator": "==",
                        "value": "-1"
                    }
                ]
            }
        }
    ],
    "results": [
        {
            "table": "variants",
            "start": "-1",
            "end": "-1",
            "referenceName": "-1"
        }
    ]
}

POST_VARIANT_SEARCH_BODY={
    "datasetId": "-1",
    "start": "-1",
    "end": "-1",
    "referenceName": "-1"
}

def get_post_search_body(input, dataset_id, patient_id):
    body = POST_SEARCH_BODY.copy()
    if patient_id is not None:
        body["components"][0]["patients"]["filters"][0]["value"] = patient_id
    else:
        body["components"][0]["patients"]["filters"][0]["value"] = "N/A"
        body["components"][0]["patients"]["filters"][0]["operator"] = "!="
    
    body["datasetId"] = dataset_id
    body["results"][0]["start"] = input.start
    body["results"][0]["end"] = input.end
    body["results"][0]["referenceName"] = input.referenceName
    return body

def get_post_variant_search_body(dataset_id, input):
    ret = POST_VARIANT_SEARCH_BODY.copy()
    ret["datasetId"] = dataset_id
    ret["start"] = input.start
    ret["end"] = input.end
    ret["referenceName"] = input.referenceName
    return ret

def _json_object_hook(d):
    return NamedTuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

def get_katsu_response(endpoint, token):
    response = requests.get(f'{api.settings.GRAPHQL_KATSU_API}/{endpoint}', headers={api.settings.GRAPHQL_KATSU_TOKEN_KEY : f"{token}"})

    if response.status_code != 200:
        response_text = response.text.replace("\n", " ")
        print(f'NON-200 response from Katsu! - {response.status_code} --- Response: {response_text}')
        raise GraphQLError("NON-200 response from Katsu!")

    return response.json()

def get_candig_server_response(endpoint, token):
    response = requests.get(f'{api.settings.GRAPHQL_CANDIG_SERVER}/{endpoint}', headers={api.settings.GRAPHQL_CANDIG_TOKEN_KEY: f"{token}"})

    if response.status_code != 200:
        response_text = response.text.replace("\n", " ")
        print(f'NON-200 response from Candig Server! - {response.status_code} --- Response: {response_text}')
        raise GraphQLError("NON-200 response from Candig Server!")

    return response.json()

def post_candig_server_response(endpoint, token, body = None):
    response = requests.post(f'{api.settings.GRAPHQL_CANDIG_SERVER}/{endpoint}', json = body, headers={api.settings.GRAPHQL_CANDIG_TOKEN_KEY: f"{token}"})
    
    if response.status_code != 200:
        response_text = response.text.replace("\n", " ")
        print(f'NON-200 response from Candig Server! - {response.status_code} --- Response: {response_text}')
        raise GraphQLError("NON-200 response from Candig Server!")

    return response.json()

def get_katsu_token(info):
    return info.context["request"].headers.get(api.settings.GRAPHQL_KATSU_TOKEN_KEY) if info.context["request"].headers.get(api.settings.GRAPHQL_KATSU_TOKEN_KEY) else ""

def get_candig_token(info):
    return info.context["request"].headers.get(api.settings.GRAPHQL_CANDIG_TOKEN_KEY) if info.context["request"].headers.get(api.settings.GRAPHQL_CANDIG_TOKEN_KEY) else ""

def gene_filter(gene, kwargs):
    id = kwargs.pop("id", None)

    if id != kwargs and id not in gene["alternate_ids"]:
        return False
    return all(item in gene.items() for item in kwargs.items())

def json_to_obj_arr(json, cast_type):
    res = []
    for x in json:
        res.append(cast_type(**x))
    return res


def generate_res(json, cast_type, kwargs, filter):
    res = []
    for x in json:
        if filter(x, kwargs):
            res.append(cast_type(**x))
    return res

def resolve_extra_properties(parent, info):
    if parent.get("extra_properties"):
        return json2obj(parent.extra_properties)
    return None

def set_field_list(json, obj, field_name, cast_type):
    field = json.get(field_name)
    if field != None:
        if isinstance(field, List):
            obj.__setattr__(field_name, [])
            for x in field:
                obj.__getattribute__(field_name).append(cast_type.deserialize(x))
        else:
            obj.__setattr__(field_name, [cast_type.deserialize(field)])

def set_field(json, obj, field_name, cast_type):
    field = json.get(field_name)
    if field != None:
        obj.__setattr__(field_name, cast_type.deserialize(field))

def set_extra_properties(json, obj):
    extra_properties = json.get("extra_properties")
    if extra_properties != None:
        obj.extra_properties = JSONScalar(extra_properties)

def set_JSON_scalar(json, obj, field_name):
    field = json.get(field_name)
    if field != None:
        obj.__setattr__(field_name, JSONScalar(field))

def generic_filter(instance, input):
    if input == None:
        return True
    
    for attr in input.__annotations__:
        attr_input_value = input.__getattribute__(attr)
        if attr_input_value != None:
            if attr == "ids" and "alternate_ids" in instance.__dir__():
                if not any(id == instance.id or id in instance.alternate_ids for id in attr_input_value):
                    return False
                continue
            if attr == "ids":
                if not any(id == instance.id for id in attr_input_value):
                    return False
                continue
            if "__module__" in attr_input_value.__dir__():
                if attr_input_value.__module__.startswith("api.schemas"):
                    attr_instance_value = instance.__getattribute__(attr)
                    if attr_instance_value: 
                        if attr_instance_value.__class__ == list: # if the instance value is a list
                            return any(single_instance for single_instance in attr_instance_value if single_instance.__class__.filter(single_instance, attr_input_value))
                        if not attr_instance_value.__class__.filter(attr_instance_value, attr_input_value): # filter the instance based on input filter
                            return False
                    else: # instance value is null but input value is not
                        return False

            else:
                if attr_input_value != instance.__getattribute__(attr):
                    return False
    return True

async def generic_resolver_helper(info, loader_name, ids, page_number):
    token = get_katsu_token(info)
    return await info.context[loader_name].load(DataLoaderInput(token, ids, page_number))

def filter_results(res, input, cast_type):
    if input:
        return [p for p in res if cast_type.filter(p, input)] 
    else:
        return res

async def generic_resolver(info, loader_name, input: Input, cast_type):
    """
    Generic resolver with given context info, data loader name, filter input,
    and result type.
    """
    if input == None: # No filter was specified
        res = await generic_resolver_helper(info, loader_name, None, None)
    else: # input filter was specified
        res = await generic_resolver_helper(info, loader_name, input.ids, input.page_number)
    return filter_results([cast_type.deserialize(p) for p in res.output], input, cast_type)

def generic_load_fn(enpoint_name):
    """
    Returns a generic loading function for data loader by specifying endpoint name
    """
    async def load_fn(param: List[DataLoaderInput]):
        ret = []
        for dataloader_input in param:
            token = dataloader_input.token
            obj_arr = list()
            # no id was specified
            if len(dataloader_input.ids) == 0:
                url = f"{enpoint_name}?page_size=10000&page={dataloader_input.page_number}"
                response = get_katsu_response(url, token)    
                return [DataLoaderOutput(response["results"])]
            # Ids were specified
            else:
                for id in dataloader_input.ids:
                    obj_arr.append(get_katsu_response(f"{enpoint_name}/{id}", token))
            ret.append(DataLoaderOutput(obj_arr))
        return ret
    return load_fn
