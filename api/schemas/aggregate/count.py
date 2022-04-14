from api.schemas.candig_server.variant import CandigServerVariantDataLoaderInput
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket
from api.schemas.katsu.mcode.mcode_packet import MCodePacket
from api.schemas.utils import generic_resolver, candig_filter

async def count_phenopackets(info, phenopacket_filter):
    return await count_katsu(info, "phenopackets_loader", phenopacket_filter, Phenopacket)

async def count_mcodepackets(info, mcodepacket_filter):
    return await count_katsu(info, "mcode_packets_loader", mcodepacket_filter, MCodePacket)

async def count_variants(info, variant_filter):
    patient_ids = get_patient_ids(variant_filter.katsu_individual)
    variants = await get_variants(info, variant_filter, patient_ids)
    individuals = await get_individuals(info, variants)
    
    for i in range(len(variants)):
        variants[i].get_katsu_individuals = individuals[i]
    
    variants = [variant for variant in variants if candig_filter(variant, variant_filter)]
    return len(variants)

def get_patient_ids(patient):
    patient_ids = patient.ids if patient is not None else [None]
    return [None] if patient_ids is None else patient_ids

async def get_variants(info, variant_filter, patient_ids):
    variants = []
    for patient_id in patient_ids:
        loader_in = CandigServerVariantDataLoaderInput(None, variant_filter, patient_id, info)
        variants.extend(await info.context["candig_server_variants_loader"].load(loader_in))
    
    return variants

async def get_individuals(info, variants):
    individuals = []
    for variant in variants:
        if callable(variant.get_katsu_individuals):
            individuals.append(await variant.get_katsu_individuals(info))
        else:
            individuals.append(variant.get_katsu_individuals)
    
    return individuals

async def count_katsu(info, loader_name, filter, cast_type):
    return len(
        await generic_resolver(
            info=info, 
            loader_name=loader_name, 
            input=filter, 
            cast_type=cast_type
        )
    )