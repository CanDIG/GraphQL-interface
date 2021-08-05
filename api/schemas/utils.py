from api.schemas.dataloader_input import DataLoaderInput
from api.schemas.scalars.json_scalar import JSONScalar
import json
import requests
from typing import List, NamedTuple
from graphql import GraphQLError
import pprint
KATSU_API = 'http://localhost:8001/api'

def _json_object_hook(d):
    return NamedTuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


def get_response(endpoint, token):
    response = requests.get(f'{KATSU_API}/{endpoint}', headers={ "X-CANDIG-LOCAL-OIDC": f"{token}"})
    if response.status_code != 200:
        raise GraphQLError("Error response from Katsu!")
    return response.json()


def get_token(info):
    # if('X-CANDIG-LOCAL-OIDC' not in info.context.headers):
    #     raise GraphQLError('Token is missing in headers')
    return info.context["request"].headers.get('X-CANDIG-LOCAL-OIDC') if info.context["request"].headers.get('X-CANDIG-LOCAL-OIDC') else "\"fuck\""


def generic_filter(set, subset):
    return all(item in set.items() for item in subset.items())


def gene_filter(gene, kwargs):
    id = kwargs.pop("id", None)
    if id != kwargs and id not in gene["alternate_ids"]:
        return False
    return all(item in gene.items() for item in kwargs.items())

def json_to_obj_arr(json, type):
    res = []
    for x in json:
        res.append(type(**x))
    return res


def generate_res(json, type, kwargs, filter):
    res = []
    for x in json:
        if filter(x, kwargs):
            res.append(type(**x))
    return res


def generic_resolve(info, kwargs, api_endpoint, type):
    token = get_token(info)
    response = get_response(api_endpoint, token)
    return generate_res(response["results"], type, kwargs, generic_filter)


def resolve_extra_properties(parent, info):
    if parent.get("extra_properties"):
        return json2obj(parent.extra_properties)
    return None

def set_field_list(json, obj, field_name, type):
    field = json.get(field_name)
    if field != None:
        obj.__setattr__(field_name, [])
        for x in field:
            obj.__getattribute__(field_name).append(type.deserialize(x))

def set_field(json, obj, field_name, type):
    field = json.get(field_name)
    if field != None:
        obj.__setattr__(field_name, type.deserialize(field))

def set_extra_properties(json, obj):
    extra_properties = json.get("extra_properties")
    if extra_properties != None:
        obj.extra_properties = JSONScalar(extra_properties)

def generic_filter(instance, input):
    if input == None:
        return True
    for attr in input.__annotations__:
        print(attr)
        attr_input_value = input.__getattribute__(attr)
        if attr_input_value != None:
            if attr == "ids" and "alternate_ids" in instance.__dir__():
                if not any(id == instance.id or id in instance.alternate_ids for id in attr):
                    return False
                continue
            if attr == "ids":
                if not any(id == instance.id for id in attr):
                    return False
                continue
            if "__module__" in attr_input_value.__dir__():
                if attr_input_value.__module__.startswith("api.schemas"):
                    attr_instance_value = instance.__getattribute__(attr)
                    if not attr_instance_value.__class__.filter(attr_instance_value, attr_input_value):
                        return False
            else:
                if attr_input_value != instance.__getattribute__(attr):
                    return False
    return True

async def generic_all_resolver(info, loader_name, input):
    token = get_token(info)
    if input == None:
        ids = None
    else:
        ids = input.ids
    res = await info.context[loader_name].load(DataLoaderInput(token, ids, input))
    return res.output