'''
    candig_to_katsu.py: transfers patient_info from CanDIG-V1 to katsu
'''

from post_data import post_candig, post_katsu
from typing import NoReturn, Dict, Any
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

    return f'Successfully Added: {patient_id}'

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
    create_post_json(patient): Passed in a JSON object patient and returns a 
        Dictionary object to use in the post request to katsu to add individuals
'''
def create_post_json(patient: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": patient.pop('patientId', None),
        "alternate_ids": [patient.pop('otherIds', None)],
        "date_of_birth": patient.pop("dateOfBirth", None),
        "sex": patient.pop("gender", 'UNKNOWN_SEX').upper(),
        "active": True,
        "deceased": True if patient.pop("dateOfDeath", None) is not None else False,
        "race": patient.pop("race", None),
        "ethnicity": patient.pop("ethnicity", None),
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