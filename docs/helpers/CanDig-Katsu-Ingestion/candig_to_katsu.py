from typing import NoReturn, Dict, Any
from defaults import *
from aiohttp import ClientSession
import asyncio

def get_dataset_id(datasets: Dict[str, Any]) -> str:
    return datasets['results']['datasets'][0]['id'].strip()


def get_patients_query(datasets: Dict[str, Any]) -> Dict[str, Any]:
    dataset_id = get_dataset_id(datasets)
    patients_query = DEFAULT_DATASET_QUERY.copy()
    patients_query['datasetId'] = dataset_id
    return patients_query


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


async def main() ->NoReturn:
    async with ClientSession() as session:
        async with session.post(f'http://{DEFAULT_HOST}:3000/datasets/search', json=DEFAULT_DATASET_QUERY) as response:
            datasets = await response.json()
        
        async with session.post(f'http://{DEFAULT_HOST}:3000/patients/search', json=get_patients_query(datasets)) as patient_response:
            patients = await patient_response.json()
        
        for patient in patients['results']['patients']:
            patient_json = create_post_json(patient)

            async with session.post(f'http://{DEFAULT_HOST}:8000/api/individuals', json=patient_json) as json_dump:
                status = await json_dump.json()
            
            if status.get('created') is None:
                print(f'ERROR in ADDING INDIVIDUAL TO KATSU: {status}')
            
if __name__ == "__main__":
    asyncio.run(main())
