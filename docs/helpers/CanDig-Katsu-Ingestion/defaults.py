DEFAULT_DATASET_QUERY = {
    "pageSize": 1000,
    "pageToken": "0"
}

DEFAULT_HOST = 'localhost'

DEFAULT_MEDICATIONS = ['MED_A', 'MED_B', 'MED_C', 'MED_D', 'MED_E']

DEFAULT_INTENTS = ['TUMOUR REDUCTION', 'TUMOUR CONTROL', 'SIDE-EFFECT MANAGEMENT']

DEFAULT_PROCEDURES = [('surgical', 'Liver Metastectomy'), ('surgical', 'Prostatectomy'), ('surgical', 'Sentinel Lymph Node Biopsy'), 
                ('surgical', 'Excision of Breast Tissue'), ('surgical', 'Partial Mastectomy'), ('surgical', 'Excision of Axillary Lymph Node'),
                ('surgical', 'Partial Resection of Colon'), ('surgical', 'Sysgenic Cell Transplant'), ('surgical', 'Right Hemicolectomy'),
                ('surgical', 'Low Anterior Resection'), ('radiation', 'Photon Radiation Therapy'), ('radiation', 'Proton Radiation Therapy'),
                ('radiation', 'Conventional External Beam')]

DEFAULT_CONDITIONS = ['Neoplasm of Prostate', 'Malignant Neoplasm of Beast', 'Malignant Tumour of Colon', 'Skin Cancer', 'Leukemia', 'Melanoma', 
                'Uterine Cancer', 'Bladder Cancer', 'Ovarian Cancer', 'Esophageal Cancer', 'Thyroid Cancer', 'Pancreatic Cancer', 'Lung Cancer',
                'Non-Hodgkin Lymphoma', 'Brain Cancer', 'Cervical Cancer', 'Kidney Cancer']

DEFAULT_STATUSES = ['Patient\'s condition improved', 'Patient\'s condition worsened']

DEFAULT_DATASET = {
        "title": "DEFAULT",
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
        "project": "PROJECT_ID"
    }

DEFAULT_TABLE = {
    "table_id": 'TABLE_ID',
    "service_id": "service",
    "dataset": 'DATASET'
}

DEFAULT_MCODE = {
    "ownership_record": "GraphQLTestDataset_mcodepacket",
    "name": "table_mcode_1",
    "data_type": "mcodepacket"
}

DEFAULT_PHENOPACKET = {
    "ownership_record": "GraphQLTestDataset_phenopacket",
    "name": "table_phenopacket_1",
    "data_type": "phenopacket"
}