from math import ceil
from typing import Optional
from fastapi import FastAPI, HTTPException
import json

# CONSTANTS
VARIANT_SET_ID_1 = "WyJ0ZXN0MzAwIiwidnMiLCJQQVRJRU5UXzkxMjUwX1NBTVBMRV84MTUxNSJd"
VARIANT_SET_ID_2 = "WyJ0ZXN0MzAwIiwidnMiLCJQQVRJRU5UXzMwNzE4X1NBTVBMRV81ODAxNCJd"
MOCK_DATASET_ID = "WyJ0ZXN0MzAwIl0"
NUMBER_OF_RECORDS = 2
PATIENT_1 = "91250"
PATIENT_2 = "30718"
VARIANT_START = 712870
VARIANT_END = 712871
VARIANT_REF = "1"

server = FastAPI()

# Helper Functions
def get_max_page(page_size):
    return ceil(NUMBER_OF_RECORDS / page_size)

# Server Endpoints
@server.get("/katsu/cancerconditions", status_code=200)
def return_cancerconditions(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/cancerconditions.json') as file:
        return json.load(file)

@server.get("/katsu/cancerrelatedprocedures", status_code=200)
def return_cancerrelatedprocedures(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/cancerrelatedprocedures.json') as file:
        return json.load(file)

@server.get("/katsu/geneticspecimens", status_code=200)
def return_geneticspecimens(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/geneticspecimens.json') as file:
        return json.load(file)

@server.get("/katsu/genomicregionsstudied", status_code=200)
def return_genomicregionsstudied(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/genomicregionsstudied.json') as file:
        return json.load(file)

@server.get("/katsu/genomicsreports", status_code=200)
def return_genomicsreports(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/genomicsreport.json') as file:
        return json.load(file)

@server.get("/katsu/individuals", status_code=200)
def return_individuals(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/individuals.json') as file:
        return json.load(file)

@server.get("/katsu/individuals/{id}", status_code=200)
def return_individuals_by_id(id):
    numeric_id = id.strip("PATIENT_").strip()
    if numeric_id == PATIENT_1 or numeric_id == PATIENT_2:
        with open(f'mocks/katsu/mcodedata/patient_{numeric_id}.json') as file:
            return json.load(file)
    
    raise HTTPException(status_code=404, detail="No such patient exists")

@server.get("/katsu/labsvital", status_code=200)
def return_labsvital(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/labsvital.json') as file:
        return json.load(file)

@server.get("/katsu/mcodepackets", status_code=200)
def return_mcodepackets(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/mcodepacket.json') as file:
        return json.load(file)

@server.get("/katsu/mcodepackets/{id}", status_code=200)
def return_mcodepackets_by_id(id):
    numeric_id = id.strip("PATIENT_").strip("_MCODE").strip()
    if numeric_id == PATIENT_1 or numeric_id == PATIENT_2:
        with open(f'mocks/katsu/mcodedata/mcodepackets_{numeric_id}.json') as file:
            return json.load(file)
    
    raise HTTPException(status_code=404, detail="No such mcodepacket exists")

@server.get("/katsu/medicationstatements", status_code=200)
def return_medicationstatements(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/medicationstatements.json') as file:
        return json.load(file)

@server.get("/katsu/phenopackets", status_code=200)
def return_phenopackets(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/phenopackets/phenopackets.json') as file:
        return json.load(file)

@server.get("/katsu/phenopackets/{id}", status_code=200)
def return_phenopackets_by_id(id):
    numeric_id = id.strip("PATIENT_").strip("_PHENOPACKET").strip()
    if numeric_id == PATIENT_1 or numeric_id == PATIENT_2:
        with open(f'mocks/katsu/phenopackets/phenopackets_{numeric_id}.json') as file:
            return json.load(file)
    
    raise HTTPException(status_code=404, detail="No such phenopacket exists")

@server.get("/katsu/tnmstaging", status_code=200)
def return_tnmstaging(page_size: int = 100000, page: int = 1):
    if (page < 1) or (page > get_max_page(page_size)):
        raise HTTPException(
            status_code=416, 
            detail="Page index out of range", 
            headers={"Content-Range": f"pages */{get_max_page(page_size)}"})
    
    with open('mocks/katsu/mcodedata/tnmstaging.json') as file:
        return json.load(file)

@server.post("/candig/search", status_code=200)
def return_candig_search(params: dict):
    dataset_id = params.get("datasetId")
    patient_id = params.get("components")[0].get("patients").get("filters")[0].get("value")
    operator = params.get("components")[0].get("patients").get("filters")[0].get("operator")
    start = params.get("results")[0].get("start")
    end = params.get("results")[0].get("end")
    reference_name = params.get("results")[0].get("referenceName")

    if dataset_id == MOCK_DATASET_ID:
        if int(start) <= VARIANT_START and int(end) >= VARIANT_END and reference_name == VARIANT_REF:
            if patient_id == f"PATIENT_{PATIENT_1}":
                with open(f'mocks/candig/variants_{PATIENT_1}.json') as file:
                    return json.load(file)
            elif patient_id == f"PATIENT_{PATIENT_2}":
                with open(f'mocks/candig/variants_{PATIENT_2}.json') as file:
                    return json.load(file)
            elif patient_id == "N/A" and operator == "!=":
                with open('mocks/candig/variants.json') as file:
                    return json.load(file)
        return {
            "status": {
                "Known peers": 1,
                "Queried peers": 1,
                "Successful communications": 1,
                "Valid response": True
            },
            "results": {
                "variants": [],
                "total": 0
            }
        }
    
    raise HTTPException(status_code=404, detail="Resource not found")

@server.post("/candig/variants/search", status_code=200)
def return_candig_variants_search(params: dict):
    datasetId = params.get('datasetId')
    referenceName = params.get('referenceName')
    start = params.get('start')
    end = params.get('end')

    if datasetId == MOCK_DATASET_ID and referenceName == VARIANT_REF and int(start) <= VARIANT_START and int(end) >= VARIANT_END:
        with open('mocks/candig/variants.json') as file:
            return json.load(file)
    
    raise HTTPException(status_code=404, detail="No such resource")

@server.post("/candig/datasets/search", status_code=200)
def return_candig_datasets_search(params: Optional[dict] = None):
    with open('mocks/candig/datasets.json') as file:
            return json.load(file)

@server.get("/candig/variantsets/{variantSetId}", status_code=200)
def return_candig_variantsets(variantSetId):
    if variantSetId == VARIANT_SET_ID_1:
        with open(f'mocks/candig/variantsets_{PATIENT_1}.json') as file:
            return json.load(file)
    elif variantSetId == VARIANT_SET_ID_2:
        with open(f'mocks/candig/variantsets_{PATIENT_2}.json') as file:
            return json.load(file)
    
    return {"results": {"patientId": "1"}}