from api.schemas.json_formats.phenopacket_external_reference import PhenopacketExternalReference, PhenopacketExternalReferenceInputType
from api.schemas.json_formats.ontology import Ontology, OntologyInputType
from api.interfaces.input import Input
from api.schemas.utils import generic_filter, set_field
from typing import Optional
import strawberry

@strawberry.input
class PhenopacketEvidenceInputType(Input):
    evidence_code: Optional[OntologyInputType] = None
    reference: Optional[PhenopacketExternalReferenceInputType] = None

@strawberry.type
class PhenopacketEvidence:
    evidence_code: Ontology
    reference: Optional[PhenopacketExternalReference] = None
    
    @staticmethod
    def deserialize(json):
        ret = PhenopacketEvidence(**json)

        for (field_name ,type) in [("evidence_code", Ontology), ("reference", PhenopacketExternalReference)]:
            set_field(json, ret, field_name, type)

        return ret
    
    @staticmethod
    def filter(instance, input: PhenopacketEvidenceInputType):
        return generic_filter(instance, input)