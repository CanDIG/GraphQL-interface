'''
    create_meta.py: File containing functions used to generate Katsu Metadata for testing purposes.
'''

from datetime import datetime
from typing import Any, Dict
from post_data import post_katsu
from defaults import DEFAULT_DATASET, DEFAULT_TABLE, DEFAULT_MCODE, DEFAULT_PHENOPACKET
import aiohttp

async def create_phenopacket_table(session: aiohttp.ClientSession) -> Dict[str, Any]:
    phenopacket_table = DEFAULT_PHENOPACKET.copy()
    return await post_katsu(session, phenopacket_table, 'tables')

async def create_mcode_table(session: aiohttp.ClientSession) -> Dict[str, Any]:
    mcode_table = DEFAULT_MCODE.copy()
    return await post_katsu(session, mcode_table, 'tables')

async def create_project(session: aiohttp.ClientSession) -> Dict[str, Any]:
    project_data = {"title": "GraphQLTestTable", "description": "Table for Testing GraphQL Queries"}
    return await post_katsu(session, project_data, 'projects')

async def create_metadata(session: aiohttp.ClientSession) -> Dict[str, Any]:
    metadata = {
        'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'created_by': "GraphQLTester",
        'submitted_by': "GraphQLTester",
        'phenopacket_schema_version': 'v1.0.0',
        'external_references': [{
            'id': 'GRAPHQL_TESTER_METADATA_REFERENCE',
            'description': 'Testable External Ref for Metadata'
        }]
    }
    return await post_katsu(session, metadata, 'metadata')

async def create_dataset(session: aiohttp.ClientSession, project_id: str, type: str) -> Dict[str, Any]:
    dataset_json = DEFAULT_DATASET.copy()
    dataset_json['title'] = f"GraphQLTestDataset_{type}"
    dataset_json['project'] = project_id

    return await post_katsu(session, dataset_json, 'datasets')

async def create_table_ownership(session: aiohttp.ClientSession, table_id: str, dataset_id: str) -> Dict[str, Any]:
    table_ownership = DEFAULT_TABLE.copy()
    table_ownership['table_id'] = table_id
    table_ownership['dataset'] = dataset_id

    return await post_katsu(session, table_ownership, 'table_ownership')

async def add_phenopackets(session: aiohttp.ClientSession, project_id: str):
    dataset = await create_dataset(session, project_id, 'phenopacket')
    dataset_id = dataset.get('identifier')
    dataset_title = dataset.get('title')

    await create_table_ownership(session, dataset_title, dataset_id)
    await create_phenopacket_table(session)


async def add_mcodepackets(session: aiohttp.ClientSession, project_id: str):
    dataset = await create_dataset(session, project_id, 'mcodepacket')
    dataset_id = dataset.get('identifier')
    dataset_title = dataset.get('title')

    await create_table_ownership(session, dataset_title, dataset_id)
    await create_mcode_table(session)