'''
Purpose: 
    Perform coverage testing of the GraphQL service by trying to return most of the fields and subfields of the 
    GraphQL BeaconV1 endpoint. Can run script through command line with `python3 test_examples.py`
'''

from typing import Any, Dict
from example_query import long_query
import aiohttp
import aiofiles
import asyncio
import json

GRAPHQL_HOST = 'http://localhost:7999/graphql'

def has_errors(response: Dict[str, Any]) -> bool:
    return response.get('errors') != None

async def main():
    async with aiofiles.open('./docs/samplequeries/example_inputs.json', mode='r') as f:
        input_json = await f.read()
    
    inputs = json.loads(input_json)['inputs']

    async with aiohttp.ClientSession() as session:
        for input in inputs:
            input_vars = {
                "rName": input['chr'],
                "rBase": input['ref_base'],
                "aBase": input['alt_base'],
                "start": int(input['start']),
                "end": int(input['end'])
            }

            async with session.post(GRAPHQL_HOST, json={"query": long_query, "variables": input_vars}) as response:
                request = await response.json()
            
            if has_errors(request):
                print(f'Error in GraphQL Query: {request.get("errors")}')
            else:
                print(f'Query # {input["id"]} passed without error! The response indicated that a variant {"exists" if request["data"]["beaconQuery"]["exists"] else "does not exist"}.')

if __name__ == "__main__":
    asyncio.run(main())