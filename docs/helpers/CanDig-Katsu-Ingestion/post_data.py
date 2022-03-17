'''
    post_data.py: File containing functions to perform POST requests to Katsu and CanDIG services for coverage testing of Beacon V1
'''

from random import randint
from generate_data import *
from defaults import *
import aiohttp

async def post_katsu(session: aiohttp.ClientSession, data: Dict[str, Any], *args) -> Dict[str, Any]:
    async with session.post(f'http://{DEFAULT_HOST}:{DEFAULT_KATSU_PORT}/api/{"/".join(args)}', json=data) as response:
        return await response.json()

async def post_candig(session: aiohttp.ClientSession, data: Dict[str, Any], *args) -> Dict[str, Any]:
    async with session.post(f'http://{DEFAULT_HOST}:{DEFAULT_CANDIG_PORT}/{"/".join(args)}', json=data) as response:
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
        "termination_reason": [{
            "id": f'{patient_id}_TR',
            "label": f'Ended medication due to reason #{randint(1, 5)}'
        }],
        "start_date": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "end_date": generate_date_after(start_date, 2015).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "extra_properties": generate_extra_properties()
    }

    return await post_katsu(session, my_medication, 'medicationstatements')

async def post_cancer_related_procedures(session: aiohttp.ClientSession, patient_id: str, condition_code: str) -> Dict[str, Any]:
    procedure_type = random.choice(DEFAULT_PROCEDURES)
    my_procs = {
        "id": f'{patient_id}_CRP',
        "procedure_type": procedure_type[0],
        "code": {
            'id': f'{patient_id}_CRP_CODE',
            'label': procedure_type[1]
        },
        "body_site": [{
            "id": f'{patient_id}_CRP_SITE',
            "label": f'Site #{randint(1, 5)} for cancer-related procedure'
        }],
        "laterality": {
            "id": f'{patient_id}_CRP_LATERALITY',
            "label": f'Laterality for CRP'
        },
        "treatment_intent": {
            'id': f'{patient_id}_CRP_INTENT',
            'label': random.choice(DEFAULT_INTENTS)
        },
        "reason_code": {
            "id": f'{patient_id}_CRP_RC',
            "label": f'Reason #{randint(1, 5)} for cancer-related procedure'
        },
        "extra_properties": generate_extra_properties(),
        "reason_reference": [condition_code]
    }

    return await post_katsu(session, my_procs, 'cancerrelatedprocedures')

async def post_cancer_condition(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_cancer_condition = {
        "id": f'{patient_id}_CC',
        "condition_type": random.choice(['primary', 'secondary']),
        "body_site": [{
            "id": f'{patient_id}_CC_SITE',
            "label": f'Site #{randint(1, 5)} for cancer condition'
        }],
        "laterality": {
            "id": f'{patient_id}_CC_LATERALITY',
            "label": f'Laterality for CC'
        },
        "clinical_status": {
            'id': f'{patient_id}_CC_STATUS',
            'label': 'active'
        },
        "code": {
            'id': f'{patient_id}_CC_CODE',
            'label': random.choice(DEFAULT_CONDITIONS)
        },
        "date_of_diagnosis": generate_date(2010, 2015).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "histology_morphology_behaviour": {
            "id": f'{patient_id}_CC_HMB',
            "label": 'HMB for CC'
        },
        "verification_status": {
            "id": f'{patient_id}_VERIFICATION_STATUS',
            "label": choice(['confirmed', 'unconfirmed', 'provisional', 'refuted', 'differential'])
        },
        "extra_properties": generate_extra_properties()
    }

    return await post_katsu(session, my_cancer_condition, 'cancerconditions')

async def post_biosample(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    year, month, day = randint(20, 60), randint(1, 11), randint(1, 30)
    my_biosample = {
        "id": f"{patient_id}_BIO",
        "procedure": {
            "code": {
                "id": f"{patient_id}_BIO_CODE",
                "label": f"PROC_{random.choice([1, 2, 3, 4, 5])}"
            },
            "body_site": {
                "id": f'{patient_id}_BIO_SITE',
                "label": f'SITE NUMBER: {random.choice([1, 2, 3, 4, 5])}'
            }
        },
        "sampled_tissue": {
            "id": f"{patient_id}_BIO_TISSUE",
            "label": f"TISSUE_{random.choice(['A', 'B', 'C'])}"
        },
        "description": f"Biosample for {patient_id}. Test Data used for GraphQL Testing",
        "individual": patient_id,
        "taxonomy": {
            "id": f'{patient_id}_BIO_TAXONOMY',
            "label": 'NCBITaxon:9606'
        },
        "individual_age_at_collection": choice([
            {"age": f'P{year}Y{month}M{day}D'},
            {"start": {"age": f'P{year - 1}Y{month}M{day}D'}, "end": {"age": f'P{year + 1}Y{month}M{day}D'}}
        ]),
        "histological_diagnosis": {
            "id": f'{patient_id}_BIO_HIST',
            "label": random.choice(['NCIT:C38757', 'NCIT:C38758'])
        },
        "tumor_progression": {
            "id": f'{patient_id}_BIO_TUMOR',
            "label": random.choice(['primary', 'metastases', 'recurrence'])
        },
        "tumor_grade": {
            "id": f'{patient_id}_BIO_GRADE',
            "label": random.choice(['NCIT:C28077', 'NCIT:C94678', 'NCIT:C28078', 'NCIT:C28079', 'NCIT:C28082'])
        },
        "diagnostic_markers": [{
            "id": f'{patient_id}_BIO_DM',
            "label": random.choice(['NCIT:C25294', 'NCIT:C68748', 'NCIT:C131711'])
        }],
        "is_control_sample": True if (random.randint(0, 100) > 95) else False
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
        }],
        "onset": generate_onset(patient_id)
    }
    return await post_katsu(session, my_diseases, 'diseases')

async def post_genes(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_genes = {
        "id": f"{patient_id}_GENES",
        "alternate_ids": [f'{int(patient_id.strip("PATIENT_"))}'],
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
        },
        "zygosity":{
            "id": f'{patient_id}_ALLELE_ZYGOSITY',
            "label": 'Allele Zygosity for given variant'
        }
    }
    return await post_katsu(session, my_variants, 'variants')

async def post_features(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_features = {
        "type": {
            "id": f'{patient_id}_PF_TYPE',
            "label": f'Phenotypic Features for {patient_id}'
        },
        "description": f'Phenotypic Features for {patient_id}',
        "negated": f'{random.choice([True, False])}',
        "severity": {
            "id": f'{patient_id}_PF_SEVERITY',
            "label": f'{random.choice(DEFAULT_SEVERITIES)}'
        },
        "modifier": [{
            "id": f'{patient_id}_PF_MODIFIER',
            "label": f'{patient_id} Modifier'
        }],
        "onset": {
            "id": f'{patient_id}_PF_ONSET',
            "label": f'{random.choice(DEFAULT_ONSETS)}'
        },
        "evidence": {
            "evidence_code": {
                "id": f'{patient_id}_PF_EVIDENCE_EVIDENCE_CODE',
                "label": f'EVIDENCE CODE: {random.randint(0, 1000)}'
            },
            "reference": {
                "id": f'{patient_id}_PF_EVIDENCE_REFERENCE',
                "description": f'Reference Description - {patient_id}'
            }
        },
        "biosample": f'{patient_id}_BIO',
        "phenopacket": f'{patient_id}_PHENOPACKET'
    }

    return await post_katsu(session, my_features, 'phenotypicfeatures')

async def post_genetic_specimens(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_specimen = {
        "id": f"{patient_id}_SPECIMEN",
        "specimen_type": {
            "id": f"{patient_id}_SPECIMEN_TYPE",
            "label": f"Random Specimen #{randint(1, 10)}"
        },
        "collection_body": {
            "id": f"{patient_id}_SPECIMEN_CB",
            "label": f"Organization #{randint(1, 10)}"
        },
        "laterality": {
            "id": f"{patient_id}_SPECIMEN_LATERALITY", 
            "label": "Laterality for SPECIMEN"
        },
        "extra_properties": generate_extra_properties()
    }

    return await post_katsu(session, my_specimen, 'geneticspecimens')

async def post_genomic_regions_studied(session: aiohttp.ClientSession, patient_id: str) -> Dict[str, Any]:
    my_region = {
        "id": f"{patient_id}_GRS",
        "dna_ranges_examined": [{
            "id": f"{patient_id}_GRS_DNA_RANGE", 
            "label": f"Start: {randint(1, 10)}; End: {randint(90, 100)}"
        }],
        "dna_region_description": [
            "Description of DNA Region"
        ],
        "gene_mutation": [{
            "id": f"{patient_id}_GRS_GENE_MUTATION", 
            "label": f"Mutation on chromosome {randint(1, 22)}"
        }],
        "gene_studied": [{
            "id": f"{patient_id}_GRS_GS", 
            "label": f"Studied Gene #{randint(1, 1000000)}"
        }],
        "genomic_reference_sequence_id": {
            "id": f"{patient_id}_GRS_ID"
        },
        "genomic_region_coordinate_system": {
            "id": f"{patient_id}_GRS_GRCS", 
            "label": "Cartesian Coordinate System"
        },
        "extra_properties": generate_extra_properties()
    }

    return await post_katsu(session, my_region, 'genomicregionsstudied')