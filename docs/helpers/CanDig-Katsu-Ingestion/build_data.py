from datetime import datetime, timedelta
import random
from typing import Any, Dict, NoReturn
import aiohttp
import asyncio

MEDICATIONS = ['MED_A', 'MED_B', 'MED_C', 'MED_D', 'MED_E']
INTENTS = ['TUMOUR REDUCTION', 'TUMOUR CONTROL', 'SIDE-EFFECT MANAGEMENT']
PROCEDURES = [('surgical', 'Liver Metastectomy'), ('surgical', 'Prostatectomy'), ('surgical', 'Sentinel Lymph Node Biopsy'), 
                ('surgical', 'Excision of Breast Tissue'), ('surgical', 'Partial Mastectomy'), ('surgical', 'Excision of Axillary Lymph Node'),
                ('surgical', 'Partial Resection of Colon'), ('surgical', 'Sysgenic Cell Transplant'), ('surgical', 'Right Hemicolectomy'),
                ('surgical', 'Low Anterior Resection'), ('radiation', 'Photon Radiation Therapy'), ('radiation', 'Proton Radiation Therapy'),
                ('radiation', 'Conventional External Beam')]
CONDITIONS = ['Neoplasm of Prostate', 'Malignant Neoplasm of Beast', 'Malignant Tumour of Colon', 'Skin Cancer', 'Leukemia', 'Melanoma', 
                'Uterine Cancer', 'Bladder Cancer', 'Ovarian Cancer', 'Esophageal Cancer', 'Thyroid Cancer', 'Pancreatic Cancer', 'Lung Cancer',
                'Non-Hodgkin Lymphoma', 'Brain Cancer', 'Cervical Cancer', 'Kidney Cancer']
STATUSES = ['Patient\'s condition improved', 'Patient\'s condition worsened']


def generate_between(date_1: datetime, date_2: datetime) -> datetime:
    days_delta = (date_2 - date_1).days
    random_day = random.randint(0, days_delta)
    date_offset = timedelta(days=random_day)
    return date_1 + date_offset


def generate_date(year_1: int, year_2: int) -> datetime:
    min_date = datetime(year_1, 1, 1)
    max_date = datetime(year_2, 12, 31)
    return generate_between(min_date, max_date)


def generate_date_after(date: datetime, max_year: int) -> datetime:
    max_date = datetime(max_year, 12, 31)
    return generate_between(date, max_date)


def generate_extra_properties() -> Dict[str, Any]:
    return {
        "dose_frequency": random.choice(['1x', '2x', '3x', '4x', '5x']),
        "route": random.choice(['IV', 'ORAL']),
        "dose": str(random.randint(1, 50)),
        "dose_unit": "mg" 
    }


async def post_medication_statement(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_medication = {}
    my_medication['id'] = f'{patient_id}_MS'
    my_medication['medication_code'] = {
        'id': f'{patient_id}_MS_CODE',
        'label': random.choice(MEDICATIONS)
    }
    my_medication['treatment_intent'] = {
        'id': f'{patient_id}_MS_INTENT',
        'label': random.choice(INTENTS)
    }
    start_date = generate_date(2010, 2015)
    my_medication['start_date'] = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    my_medication['end_date'] = generate_date_after(start_date, 2015).strftime('%Y-%m-%dT%H:%M:%SZ')
    my_medication['extra_properties'] = generate_extra_properties()

    async with session.post('http://192.168.68.120:8000/api/medicationstatements', json=my_medication) as response:
        return await response.json()

async def get_medication_statement(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    async with session.get(f'http://192.168.68.120:8000/api/medicationstatements/{patient_id}_MS') as response:
        return await response.json()

async def post_cancer_related_procedures(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_procs = {}
    my_procs['id'] = f'{patient_id}_CRP'
    procedure_type = random.choice(PROCEDURES)
    my_procs['procedure_type'] = procedure_type[0]
    my_procs['code'] = {
        'id': f'{patient_id}_CRP_CODE',
        'label': procedure_type[1]
    }
    my_procs['treatment_intent'] = {
        'id': f'{patient_id}_CRP_INTENT',
        'label': random.choice(INTENTS)
    }
    async with session.post('http://192.168.68.120:8000/api/cancerrelatedprocedures', json=my_procs) as response:
        return await response.json()

async def get_cancer_related_procedures(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    async with session.get(f'http://192.168.68.120:8000/api/cancerrelatedprocedures/{patient_id}_CRP') as response:
        return await response.json()

async def post_cancer_condition(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_cancer_condition = {}
    my_cancer_condition['id'] = f'{patient_id}_CC'
    my_cancer_condition['condition_type'] = random.choice(['primary', 'secondary'])
    my_cancer_condition['clinical_status'] = {
        'id': f'{patient_id}_CC_STATUS',
        'label': 'active'
    }
    my_cancer_condition['code'] = {
        'id': f'{patient_id}_CC_CODE',
        'label': random.choice(CONDITIONS)
    }
    my_cancer_condition['date_of_diagnosis'] = generate_date(2010, 2015).strftime('%Y-%m-%dT%H:%M:%SZ')

    async with session.post('http://192.168.68.120:8000/api/cancerconditions', json=my_cancer_condition) as response:
        return await response.json()

async def get_cancer_condition(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    async with session.get(f'http://192.168.68.120:8000/api/cancerconditions/{patient_id}_CC') as response:
        return await response.json()

def id_exists(statement: Dict[str, Any]) -> bool:
    if isinstance(statement.get('id'), list) and 'id already exists' in statement.get('id')[0]:
        return True
    return False

def generate_mcodepacket(patient_id: str, medication_id: str, procedures_id: str, cancer_condition_id: str, table_id: str) -> Dict[str, Any]:
    return {
        'id': f'{patient_id}_MCODE',
        'date_of_death': generate_date(2016, 2021).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'cancer_disease_status': {
            'id': f'{patient_id}_MCODE_STATUS',
            'label': random.choice(STATUSES)
        }, 'subject': patient_id,
        'cancer_condition': [cancer_condition_id],
        'cancer_related_procedures': [procedures_id],
        'medication_statement': [medication_id],
        'extra_properties': {
            'height': str(round(random.gauss(175, 7))) + 'cm',
            'weight': str(random.randint(45, 90)) + 'kg'
            },
        'table': table_id
    }

def print_result(patient_id:str, response: Dict[str, Any]) -> NoReturn:
    if response.get('id') is None:
        print(f'Failed to Add mCODE packet to Katsu API for {patient_id}. Response: {response}')
    elif id_exists(response):
        print(f'{patient_id} already added to Katsu. Response: {response}')
    else:
        print(f'Successfully added {patient_id}')

async def update_mcode(patient_id: str, session: aiohttp.ClientSession, table_id: str) -> NoReturn:
    medication_statement = await post_medication_statement(session, patient_id)
    if id_exists(medication_statement):
        medication_statement = await get_medication_statement(session, patient_id)
    medication_id = medication_statement.get('id')
    
    procedures = await post_cancer_related_procedures(session, patient_id)
    if id_exists(procedures):
        procedures = await get_cancer_related_procedures(session, patient_id)
    procedures_id = procedures.get('id')

    cancer_condition = await post_cancer_condition(session, patient_id)
    if id_exists(cancer_condition):
        cancer_condition = await get_cancer_condition(session, patient_id)
    cancer_condition_id = cancer_condition.get('id')

    mcode = generate_mcodepacket(patient_id, medication_id, procedures_id, cancer_condition_id, table_id)
    async with session.post('http://192.168.68.120:8000/api/mcodepackets', json=mcode) as response:
        response_json = await response.json()
    
    print_result(patient_id, response_json)


async def get_candig_patients(session: aiohttp.ClientSession):
    DEFAULT_QUERY = {"pageSize": 1000, "pageToken": "0"}
    async with session.post('http://192.168.68.120:3000/datasets/search', json=DEFAULT_QUERY) as response:
        dataset_response = await response.json()
    
    dataset_id = dataset_response['results']['datasets'][0]['id']
    DEFAULT_QUERY['datasetId'] = dataset_id

    async with session.post('http://192.168.68.120:3000/patients/search', json=DEFAULT_QUERY) as response:
        patients_response = await response.json()
    
    return [patient['patientId'] for patient in patients_response['results']['patients']]


async def post_katsu(session: aiohttp.ClientSession, data: Dict[str, Any], *args) -> Dict[str, Any]:
    async with session.post(f'http://192.168.68.120:8000/api/{"/".join(args)}', json=data) as response:
        return await response.json()


async def post_biosample(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_biosample = {
        "id": f"{patient_id}_BIO",
        "procedure": {
            "code": {
                "id": f"{patient_id}_BIO_CODE",
                "label": f"PROC_{random.choice([1, 2, 3, 4, 5])}"
            }
        },
        "sampled_tissue": {
            "id": f"{patient_id}_BIO_TISSUE",
            "label": f"TISSUE_{random.choice(['A', 'B', 'C'])}"
        },
        "description": f"Biosample for {patient_id}. Test Data used for GraphQL Testing",
        "individual": patient_id
    }

    return await post_katsu(session, my_biosample, 'biosamples')


async def post_diseases(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_diseases = {
        "term": {
            "id": f"{patient_id}_DISEASES_TERM",
            "label": f"DISEASE_TERM_{random.choice([1, 2, 3, 4 , 5])}"
        },
        "disease_stage": [{
            "id": f"{patient_id}_DISEASES_STAGE",
            "label": f"STAGE_{random.randint(1, 4)}"
        }],
        "tnm_finding": [{
            "id": f"{patient_id}_TNM",
            "label": f"TUMOUR_STAGE_{random.randint(0, 3)}"
        }]
    }
    return await post_katsu(session, my_diseases, 'diseases')

def random_letter() -> str:
    return random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'))

def random_gene_name(length: int) -> str:
    return ''.join([random_letter() for _ in range(1, length)])

async def post_genes(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_genes = {
        "id": f"{patient_id}_GENES",
        "symbol": f"{random_gene_name(5)}"
    }
    
    return await post_katsu(session, my_genes, 'genes')

async def post_variants(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    bases = ['A', 'C', 'T', 'G']
    reference_base = random.choice(bases)
    bases.remove(reference_base)
    alternate_base = random.choice(bases)

    my_variants = {
        "allele_type": "hgvsAllele",
        "allele": {
            "id": f"{patient_id}_VARIANTS_ALLELE",
            "hgvs": f"Allele Variant for {patient_id}",
            "chr": f"{random.randint(1, 22)}",
            "pos": random.randint(1, 5000000),
            "ref": f"{reference_base}",
            "alt": f"{alternate_base}"
        }
    }
    return await post_katsu(session, my_variants, 'variants')

async def get_katsu(session: aiohttp.ClientSession, *args) -> Dict[str, Any]:
    async with session.get(f'http://192.168.68.120:8000/api/{"/".join(args)}') as response:
        return await response.json()

async def get_biosample(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    return await get_katsu(session, 'biosamples', f'{patient_id}_BIO')

async def get_genes(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    return await get_katsu(session, 'genes', f'{patient_id}_GENES')

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

    my_phenopacket = {
        "id": f"{patient_id}_PHENOPACKET",
        "subject": patient_id,
        "meta_data": metadata_id,
        "biosamples": [f'{biosample_id}'],
        "genes": [f'{genes_id}'],
        "variants": [f'{variant_id}'],
        "diseases": [f'{disease_id}'],
        "table": table_id
    }
    
    response_json = await post_katsu(session, my_phenopacket, 'phenopackets')
    print(response_json)
    print_result(patient_id, response_json)

async def create_phenopacket_table(session: aiohttp.ClientSession):
    phenopacket_table = {
        "ownership_record": "GraphQLTestDataset_phenopacket",
        "name": "table_phenopacket_1",
        "data_type": "phenopacket"
    }

    return await post_katsu(session, phenopacket_table, 'tables')

async def create_mcode_table(session: aiohttp.ClientSession):
    mcode_table = {
        "ownership_record": "GraphQLTestDataset_mcodepacket",
        "name": "table_mcode_1",
        "data_type": "mcodepacket"
    }

    return await post_katsu(session, mcode_table, 'tables')

async def create_project(session: aiohttp.ClientSession) -> Dict[str, Any]:
    project_data = {"title": "GraphQLTestTable", "description": "Table for Testing GraphQL Queries"}
    return await post_katsu(session, project_data, 'projects')

async def create_metadata(session: aiohttp.ClientSession) -> Dict[str, Any]:
    return await post_katsu(session, {'created_by': "GraphQLTester"}, 'metadata')

async def create_dataset(session: aiohttp.ClientSession, project_id: str, type: str) -> Dict[str, Any]:
    dataset_json = {
        "title": f"GraphQLTestDataset_{type}",
        "data_use": {
            "consent_code": {
                "primary_category": {
                    "code": "GRU"
                },
                "secondary_categories": [
                    {
                        "code": "GSO"
                    }
                ]
            },
            "data_use_requirements": [
                {
                    "code": "COL"
                },
                {
                    "code": "PUB"
                }
            ]
        },
        "project": project_id
    }

    return await post_katsu(session, dataset_json, 'datasets')

async def create_table_ownership(session: aiohttp.ClientSession, table_id: str, dataset_id: str) -> Dict[str, Any]:
    table_ownership = {
        "table_id": table_id,
        "service_id": "service",
        "dataset": dataset_id
    }

    return await post_katsu(session, table_ownership, 'table_ownership')


async def add_phenopackets(session: aiohttp.ClientSession, project_id: str) -> str:
    dataset = await create_dataset(session, project_id, 'phenopacket')
    dataset_id = dataset.get('identifier')
    dataset_title = dataset.get('title')

    await create_table_ownership(session, dataset_title, dataset_id)
    await create_phenopacket_table(session)


async def add_mcode_packets(session, project_id):
    dataset = await create_dataset(session, project_id, 'mcodepacket')
    dataset_id = dataset.get('identifier')
    dataset_title = dataset.get('title')

    print(dataset)

    print(await create_table_ownership(session, dataset_title, dataset_id))
    print(await create_mcode_table(session))


async def add_to_katsu() -> NoReturn:
    async with aiohttp.ClientSession() as session:
        project = await create_project(session)
        project_id = project.get('identifier')

        print(project)

        metadata = await create_metadata(session)
        metadata_id = metadata.get('id')

        print(metadata)

        patients = await get_candig_patients(session)

        await add_phenopackets(session, project_id)
        await add_mcode_packets(session, project_id)

        for patient in patients:
            await update_phenopackets(patient, session, 'GraphQLTestDataset_phenopacket', metadata_id)
        
        for patient in patients:
            await update_mcode(patient, session, 'GraphQLTestDataset_mcodepacket')


if __name__ == "__main__":
    asyncio.run(add_to_katsu())