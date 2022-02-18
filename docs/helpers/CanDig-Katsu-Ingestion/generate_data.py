'''
    generate_data.py: File used to randomly generate mcode and phenopacket data for use in coverage testing of the BEacon V1 endpoint
'''

from datetime import datetime, timedelta
from defaults import DEFAULT_STATUSES
from typing import Any, Dict
import random

def generate_date_between(date_1: datetime, date_2: datetime) -> datetime:
    days_delta = (date_2 - date_1).days
    random_day = random.randint(0, days_delta)
    date_offset = timedelta(days=random_day)
    return date_1 + date_offset

def generate_date(year_1: int, year_2: int) -> datetime:
    min_date = datetime(year_1, 1, 1)
    max_date = datetime(year_2, 12, 31)
    return generate_date_between(min_date, max_date)

def generate_date_after(date: datetime, max_year: int) -> datetime:
    max_date = datetime(max_year, 12, 31)
    return generate_date_between(date, max_date)

def generate_extra_properties() -> Dict[str, Any]:
    return {
        "dose_frequency": random.choice(['1x', '2x', '3x', '4x', '5x']),
        "route": random.choice(['IV', 'ORAL']),
        "dose": str(random.randint(1, 50)),
        "dose_unit": "mg" 
    }

def generate_mcodepacket(patient_id: str, medication_id: str, procedures_id: str, cancer_condition_id: str, table_id: str) -> Dict[str, Any]:
    return {
        'id': f'{patient_id}_MCODE',
        'date_of_death': generate_date(2016, 2021).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'cancer_disease_status': {
            'id': f'{patient_id}_MCODE_STATUS',
            'label': random.choice(DEFAULT_STATUSES)
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

def generate_phenopacket(patient: str, metadata: str, table: str, biosample: str, genes: str, variant: str, disease: str) -> Dict[str, Any]:
    return {
        "id": f"{patient}_PHENOPACKET",
        "subject": patient,
        "meta_data": metadata,
        "biosamples": [f'{biosample}'],
        "genes": [f'{genes}'],
        "variants": [f'{variant}'],
        "diseases": [f'{disease}'],
        "table": table
    }

def generate_random_letter() -> str:
    return random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'))

def generate_gene_name(length: int) -> str:
    return ''.join([generate_random_letter() for _ in range(1, length)])