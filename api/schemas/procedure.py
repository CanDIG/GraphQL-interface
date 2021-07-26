from typing import Optional
from api.schemas.scalars.json_scalar import JSONScalar
import strawberry
from api.schemas.json_formats.ontology import Ontology, OntologyInputType, filter_ontology

@strawberry.input
class ProcedureInputType:
    code: Optional[OntologyInputType] = None
    body_site: Optional[OntologyInputType] = None

@strawberry.type
class Procedure:
    code: Ontology
    body_site: Ontology
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def code(self, info) -> Ontology:
        return self.code

    @strawberry.field
    def body_site(self, info) -> Ontology:
        return self.body_site

    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties

def filter_procedure(instance, input):
    code = input.get("code")
    body_site = input.get("body_site")
    if code != None and body_site != None:
        return filter_ontology(code) and filter_ontology(body_site)
    if code == None:
        return filter_ontology(body_site)
    if body_site == None:
        return filter_ontology(code)
    return True