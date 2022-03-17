'''
    build_data.py: Script used to ingest random mCODE and phenopacket data into Katsu
'''

from typing import Any, Dict, NoReturn
from candig_to_katsu import transfer_to_katsu
from generate_data import *
from create_meta import *
from get_data import *
from post_data import *
import aiohttp
import asyncio

'''
    print_result(patient_id, response, type): Passed in two strings, patient_id  & type, as well 
        as a JSON response object, response, and prints output as to whether 
        the resource was successfully added to Katsu or not
'''
def print_result(patient_id: str, response: Dict[str, Any], type: str) -> NoReturn:
    if response.get('id') is None:
        print(f'Failed to add {type} to Katsu API for {patient_id}. Response: {response}')
    elif id_exists(response):
        print(f'{patient_id}\'s {type} already added to Katsu. Response: {response}')
    else:
        print(f'Successfully added {patient_id}\'s {type}')

'''
    id_exists(statement): Passed in a JSON response, statement, and returns a 
        boolean as to whether the id exists in Katsu already or not
'''
def id_exists(statement: Dict[str, Any]) -> bool:
    if isinstance(statement.get('id'), list) and 'id already exists' in statement.get('id')[0]:
        return True
    
    return False

'''
    update_mcode(patient_id, session, table_id): Passed in patient_id & table_id, two
        strings as well as an async clientSession object, session and adds an 
        mcodepacket holding the randomly-generated data for patient_id
'''
async def update_mcode(patient_id: str, session: aiohttp.ClientSession, table_id: str) -> NoReturn:
    medication_statement = await post_medication_statement(session, patient_id)
    if id_exists(medication_statement):
        medication_statement = await get_medication_statement(session, patient_id)
    medication_id = medication_statement.get('id')

    cancer_condition = await post_cancer_condition(session, patient_id)
    if id_exists(cancer_condition):
        cancer_condition = await get_cancer_condition(session, patient_id)
    cancer_condition_id = cancer_condition.get('id')
    
    procedures = await post_cancer_related_procedures(session, patient_id, cancer_condition_id)
    if id_exists(procedures):
        procedures = await get_cancer_related_procedures(session, patient_id)
    procedures_id = procedures.get('id')

    mcode = generate_mcodepacket(patient_id, medication_id, procedures_id, cancer_condition_id, table_id)
    response_json = await post_katsu(session, mcode, 'mcodepackets')
    
    print_result(patient_id, response_json, 'mcodepacket')

'''
    update_phenopackets(patient_id, session, table_id, metadata_id): Passed in several strings
        holding ids, like table_id, metadata_id and patient_id and also passed an async ClientSession object
        session, and adds a phenopacket in Katsu holding the randomly-generated data for patient_id
'''
async def update_phenopackets(patient_id: str, session: aiohttp.ClientSession, table_id: str, metadata_id: str) -> NoReturn:
    biosample = await post_biosample(session, patient_id)
    if id_exists(biosample):
        biosample = await get_biosample(session, patient_id)
    biosample_id = biosample.get('id')

    diseases = await post_diseases(session, patient_id)
    disease_id = diseases.get('id')

    genes = await post_genes(session, patient_id)
    if id_exists(genes):
        genes = await get_genes(session, patient_id)
    genes_id = genes.get('id')

    variants = await post_variants(session, patient_id)
    variant_id = variants.get('id')

    my_phenopacket = generate_phenopacket(patient_id, metadata_id, table_id, biosample_id, genes_id, variant_id, disease_id)
    
    response_json = await post_katsu(session, my_phenopacket, 'phenopackets')

    await post_features(session, patient_id)
    print_result(patient_id, response_json, 'phenopacket')

'''
    add_to_katsu(): Transfers patient_info from the CanDIG-V1 server to Katsu, and
        adds phenopacket/mCODE data for each patient into Katsu
'''
async def add_to_katsu():
    async with aiohttp.ClientSession() as session:
        await transfer_to_katsu()

        project = await create_project(session)
        project_id = project.get('identifier')

        metadata = await create_metadata(session)
        metadata_id = metadata.get('id')

        patients = await get_candig_patients(session)

        await add_phenopackets(session, project_id)
        await add_mcodepackets(session, project_id)

        for patient in patients:
            await update_phenopackets(patient, session, 'GraphQLTestDataset_phenopacket', metadata_id)
        
        for patient in patients:
            await update_mcode(patient, session, 'GraphQLTestDataset_mcodepacket')

if __name__ == "__main__":
    asyncio.run(add_to_katsu())