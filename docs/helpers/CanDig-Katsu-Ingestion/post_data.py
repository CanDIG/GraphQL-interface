from generate_data import *
from defaults import *
import aiohttp

async def post_katsu(session: aiohttp.ClientSession, data: Dict[str, Any], *args) -> Dict[str, Any]:
    async with session.post(f'http://{DEFAULT_HOST}:8000/api/{"/".join(args)}', json=data) as response:
        return await response.json()

async def post_candig(session: aiohttp.ClientSession, data: Dict[str, Any], *args) -> Dict[str, Any]:
    async with session.post(f'http://{DEFAULT_HOST}:3000/{"/".join(args)}', json=data) as response:
        return await response.json()

async def post_medication_statement(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    start_date = generate_date(2010, 2015)
    my_medication = {
        "id": f'{patient_id}_MS',
        "medication_code": {
            "id": f'{patient_id}_MS_CODE',
            "label": random.choice(DEFAULT_MEDICATIONS)
        },
        "treatment_intent": {
            'id': f'{patient_id}_MS_INTENT',
            'label': random.choice(DEFAULT_INTENTS)
        },
        "start_date": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "end_date": generate_date_after(start_date, 2015).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "extra_properties": generate_extra_properties()
    }

    return await post_katsu(session, my_medication, 'medicationstatements')

async def post_cancer_related_procedures(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    procedure_type = random.choice(DEFAULT_PROCEDURES)
    my_procs = {
        "id": f'{patient_id}_CRP',
        "procedure_type": procedure_type[0],
        "code": {
            'id': f'{patient_id}_CRP_CODE',
            'label': procedure_type[1]
        },
        "treatment_intent": {
            'id': f'{patient_id}_CRP_INTENT',
            'label': random.choice(DEFAULT_INTENTS)
        }
    }

    return await post_katsu(session, my_procs, 'cancerrelatedprocedures')

async def post_cancer_condition(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_cancer_condition = {
        "id": f'{patient_id}_CC',
        "condition_type": random.choice(['primary', 'secondary']),
        "clinical_status": {
            'id': f'{patient_id}_CC_STATUS',
            'label': 'active'
        },
        "code": {
            'id': f'{patient_id}_CC_CODE',
            'label': random.choice(DEFAULT_CONDITIONS)
        },
        "date_of_diagnosis": generate_date(2010, 2015).strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    return await post_katsu(session, my_cancer_condition, 'cancerconditions')

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

async def post_genes(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_genes = {
        "id": f"{patient_id}_GENES",
        "symbol": f"{generate_gene_name(5)}"
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