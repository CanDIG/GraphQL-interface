import json
import requests
from typing import NamedTuple
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
    return info.context.headers.get('X-CANDIG-LOCAL-OIDC') if info.context.headers.get('X-CANDIG-LOCAL-OIDC') else "\"fuck\""


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