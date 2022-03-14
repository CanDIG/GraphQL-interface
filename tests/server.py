from typing import Optional
from fastapi import FastAPI, HTTPException
import json

server = FastAPI()

@server.get("/katsu/cancerconditions", status_code=200)
def return_cancerconditions(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/cancerconditions.json') as file:
        return json.load(file)

@server.get("/katsu/cancerrelatedprocedures", status_code=200)
def return_cancerrelatedprocedures(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/cancerrelatedprocedures.json') as file:
        return json.load(file)

@server.get("/katsu/geneticspecimens", status_code=200)
def return_geneticspecimens(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/geneticspecimens.json') as file:
        return json.load(file)

@server.get("/katsu/genomicregionsstudied", status_code=200)
def return_genomicregionsstudied(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/genomicregionsstudied.json') as file:
        return json.load(file)

@server.get("/katsu/genomicsreports", status_code=200)
def return_genomicsreports(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/genomicsreport.json') as file:
        return json.load(file)

@server.get("/katsu/individuals", status_code=200)
def return_individuals(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/individuals.json') as file:
        return json.load(file)

@server.get("/katsu/individuals/{id}", status_code=200)
def return_individuals_by_id(id):
    numeric_id = id.strip("PATIENT_").strip()
    if numeric_id == "91250" or numeric_id == "30718":
        with open(f'mocks/katsu/mcodedata/patient_{numeric_id}.json') as file:
            return json.load(file)
    
    raise HTTPException(status_code=404, detail="No such patient exists")

@server.get("/katsu/labsvital", status_code=200)
def return_labsvital(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/labsvital.json') as file:
        return json.load(file)

@server.get("/katsu/mcodepackets", status_code=200)
def return_mcodepackets(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/mcodepacket.json') as file:
        return json.load(file)

@server.get("/katsu/mcodepackets/{id}", status_code=200)
def return_mcodepackets_by_id(id):
    numeric_id = id.strip("PATIENT_").strip("_MCODE").strip()
    if numeric_id == "91250" or numeric_id == "30718":
        with open(f'mocks/katsu/mcodedata/mcodepackets_{numeric_id}.json') as file:
            return json.load(file)
    
    raise HTTPException(status_code=404, detail="No such mcodepacket exists")

@server.get("/katsu/medicationstatements", status_code=200)
def return_medicationstatements(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/mcodedata/medicationstatements.json') as file:
        return json.load(file)

@server.get("/katsu/phenopackets", status_code=200)
def return_phenopackets(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
    with open('mocks/katsu/phenopackets/phenopackets.json') as file:
        return json.load(file)

@server.get("/katsu/phenopackets/{id}", status_code=200)
def return_phenopackets_by_id(id):
    numeric_id = id.strip("PATIENT_").strip("_PHENOPACKET").strip()
    if numeric_id == "91250" or numeric_id == "30718":
        with open(f'mocks/katsu/phenopackets/phenopackets_{numeric_id}.json') as file:
            return json.load(file)
    
    raise HTTPException(status_code=404, detail="No such phenopacket exists")

@server.get("/katsu/tnmstaging", status_code=200)
def return_tnmstaging(page_size: int = 100000, page: int = 1):
    if page != 1:
        raise HTTPException(status_code=404, detail="Page index out of range")
    
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

    if int(start) <= 712870 and int(end) >= 712871 and reference_name == "1" and patient_id == "PATIENT_91250" and dataset_id == "WyJ0ZXN0MzAwIl0":
        with open('mocks/candig/variants_91250.json') as file:
            return json.load(file)
    elif int(start) <= 712870 and int(end) >= 712871 and reference_name == "1" and patient_id == "PATIENT_30718" and dataset_id == "WyJ0ZXN0MzAwIl0":
        with open('mocks/candig/variants_30718.json') as file:
            return json.load(file)
    elif int(start) <= 712870 and int(end) >= 712871 and reference_name == "1" and patient_id == "N/A" and operator == "!=" and dataset_id == "WyJ0ZXN0MzAwIl0":
        with open('mocks/candig/variants.json') as file:
            return json.load(file)
    elif dataset_id == "WyJ0ZXN0MzAwIl0":
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

    if datasetId == 'WyJ0ZXN0MzAwIl0' and referenceName == '1' and int(start) <= 712870 and int(end) >= 712871:
        with open('mocks/candig/variants.json') as file:
            return json.load(file)
    
    raise HTTPException(status_code=404, detail="No such resource")

@server.post("/candig/datasets/search", status_code=200)
def return_candig_datasets_search(params: Optional[dict] = None):
    with open('mocks/candig/datasets.json') as file:
            return json.load(file)

@server.get("/candig/variantsets/{variantSetId}", status_code=200)
def return_candig_variantsets(variantSetId):
    if variantSetId == "WyJ0ZXN0MzAwIiwidnMiLCJQQVRJRU5UXzkxMjUwX1NBTVBMRV84MTUxNSJd":
        with open('mocks/candig/variantsets_91250.json') as file:
            return json.load(file)
    elif variantSetId == "WyJ0ZXN0MzAwIiwidnMiLCJQQVRJRU5UXzMwNzE4X1NBTVBMRV81ODAxNCJd":
        with open('mocks/candig/variantsets_30718.json') as file:
            return json.load(file)
    
    return {"results": {"patientId": "1"}}