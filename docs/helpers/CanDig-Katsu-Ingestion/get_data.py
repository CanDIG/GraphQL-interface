'''
    get_data.py: File containing functions to perform GET requests to Katsu and CanDIG services for coverage testing of Beacon V1
'''

from defaults import DEFAULT_HOST, DEFAULT_DATASET_QUERY, DEFAULT_KATSU_PORT
from post_data import post_candig
from typing import Dict, Any
import aiohttp

async def get_katsu(session: aiohttp.ClientSession, *args) -> Dict[str, Any]:
    async with session.get(f'http://{DEFAULT_HOST}:{DEFAULT_KATSU_PORT}/api/{"/".join(args)}') as response:
        return await response.json()

async def get_medication_statement(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    return await get_katsu(session, 'medicationstatements', f'{patient_id}_MS')

async def get_cancer_related_procedures(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    return await get_katsu(session, 'cancerrelatedprocedures', f'{patient_id}_CRP')

async def get_cancer_condition(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    return await get_katsu(session, 'cancerconditions', f'{patient_id}_CC')

async def get_biosample(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    return await get_katsu(session, 'biosamples', f'{patient_id}_BIO')

async def get_genes(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    return await get_katsu(session, 'genes', f'{patient_id}_GENES')

async def get_candig_patients(session: aiohttp.ClientSession):
    dataset_response = await post_candig(session, DEFAULT_DATASET_QUERY, 'datasets', 'search')
    dataset_id = dataset_response['results']['datasets'][2]['id']

    patient_query = DEFAULT_DATASET_QUERY.copy()
    patient_query['datasetId'] = dataset_id

    patients_response = await post_candig(session, patient_query, 'patients', 'search')
    return [patient['patientId'] for patient in patients_response['results']['patients']]