import time
from typing import Any, Dict
import aiohttp
import asyncio

CANDIG_SERVER = 'http://localhost:3000'
KATSU_API = 'http://localhost:8000/api'
DEFAULT_JSON = {
    "pageSize": 1000,
    "pageToken": "0"
}


def get_dataset_id(datasets: Dict[str, Any]) -> str:
    return datasets['results']['datasets'][0]['id'].strip()


def create_variant_search(dataset_id):
    return {
        "datasetId": dataset_id,
        "referenceName": "1",
        "start": "712800",
        "end": "712900",
        "pageSize": 1000,
        "pageToken": "0"
}


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{CANDIG_SERVER}/datasets/search', json=DEFAULT_JSON) as dataset_response:
            dataset = await dataset_response.json()
        
        dataset_id = get_dataset_id(dataset)
        
        async with session.post(f'{CANDIG_SERVER}/variants/search', json=create_variant_search(dataset_id)) as variants_response:
            variants = await variants_response.json()
            
        patients = []
        for variant in variants['results']['variants']:
            set_id = variant['variantSetId']
            
            async with session.get(f'{CANDIG_SERVER}/variantsets/{set_id}') as variant_set_response:
                variant_set_id = await variant_set_response.json()
            
            patient_id = variant_set_id['results']['patientId']

            async with session.get(f'{KATSU_API}/individuals/{patient_id}') as individual_response:
                individual = await individual_response.json()
            
            if 'T' == variant['referenceBases'] and 'C' in variant['alternateBases']:
                patients.append(individual['date_of_birth'])
        
        print(patients)


if __name__ == "__main__":
    t1 = time.time()
    asyncio.run(main())
    print(f'Execution took: {time.time() - t1}s')