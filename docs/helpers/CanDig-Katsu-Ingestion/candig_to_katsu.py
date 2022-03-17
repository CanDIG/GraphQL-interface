'''
    candig_to_katsu.py: transfers patient_info from CanDIG-V1 to katsu
'''

from random import choice
from datetime import datetime
from post_data import post_candig, post_katsu
from typing import NoReturn, Dict, Any, Optional
from aiohttp import ClientSession
from defaults import *
import asyncio

'''
    check_response(status, patient_id): Passed in a JSON response, status
        as well as a patient_id as a string, and returns a message based on
        the status message
'''
def check_response(status: Dict[str, Any], patient_id: str) -> NoReturn:
    if status.get('created') is None:
        return f'ERROR in ADDING INDIVIDUAL TO KATSU: {status}'

    return f'Successfully Transferred: {patient_id}'

'''
    get_dataset_id(datasets): Passed in a JSON object datasets, and returns
        the patient_id
'''
def get_dataset_id(datasets: Dict[str, Any]) -> str:
    return datasets['results']['datasets'][2]['id'].strip()

'''
    get_patients_query(datasets): Passed in a JSON object, datasets, and
        returns a modified dictionary to use in a query to get all the patients
'''
def get_patients_query(datasets: Dict[str, Any]) -> Dict[str, Any]:
    dataset_id = get_dataset_id(datasets)
    patients_query = DEFAULT_DATASET_QUERY.copy()
    patients_query['datasetId'] = dataset_id
    return patients_query

'''
    get_age(birth_date, death_date): Passed in two strings corresponding to the birth and death
        dates of an individual and returns a dict containing age information of the person at the time of death/now
'''
def get_age(birth_date: Optional[str], death_date: Optional[str]) -> Optional[Dict[str, Any]]:
    if birth_date is None or death_date is None:
        return None
    
    start_date = datetime.strptime(birth_date, '%Y-%m-%d') if birth_date is not None else datetime(1950, 1, 1)
    end_date = datetime.strptime(death_date, '%Y-%m-%d') if death_date is not None else datetime.now()
    total = (end_date - start_date).days
    years = total // 365
    months = (total - (years * 365)) // 30
    days = total - (years * 365) - (months * 30)

    return choice([
            {
                "age": f'P{years}Y{months}M{days}D'
            },
            {
                "start": {
                    "age": f'P{years - 1}Y{months}M{days}D'
                },
                "end": {
                    "age": f'P{years + 1}Y{months}M{days}D'
                }
            }
        ])


'''
    create_post_json(patient): Passed in a JSON object patient and returns a 
        Dictionary object to use in the post request to katsu to add individuals
'''
def create_post_json(patient: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": patient.get('patientId', None),
        "alternate_ids": [patient.pop('otherIds', None)],
        "date_of_birth": patient.get("dateOfBirth", None),
        "sex": patient.pop("gender", 'UNKNOWN_SEX').upper(),
        "taxonomy": {
            "id": f'{patient.get("patientId", None)}_TAXONOMY',
            "label": 'NCBITaxon:9606'
        },
        "active": True,
        "deceased": True if patient.get("dateOfDeath", None) is not None else False,
        "comorbidCondition": {
            "clinical_status": {
                "id": f'{patient.get("patientId", None)}_CC_CS',
                "label": choice(['Stable', 'Critical'])
            },
            "code": {
                "id": f'{patient.get("patientId", None)}_CC_C',
                "label": f'Comorbid Condition for {patient.pop("patientId", None)}'
            }
        },
        "race": patient.pop("race", None),
        "ethnicity": patient.pop("ethnicity", None),
        "age": get_age(patient.pop('dateOfBirth', None), patient.get('dateOfDeath', None)),
        "extra_properties": {**patient}
    }

'''
    transfer_to_katsu(): Transfers patient_info from CanDIG-V1 to Katsu
'''
async def transfer_to_katsu():
    async with ClientSession() as session:
        datasets = await post_candig(session, DEFAULT_DATASET_QUERY, 'datasets', 'search')
        patients = await post_candig(session, get_patients_query(datasets), 'patients', 'search')
        
        for patient in patients['results']['patients']:
            patient_json = create_post_json(patient)
            status = await post_katsu(session, patient_json, 'individuals')
            print(check_response(status, patient_json.get('id')))
            
if __name__ == "__main__":
    asyncio.run(transfer_to_katsu())