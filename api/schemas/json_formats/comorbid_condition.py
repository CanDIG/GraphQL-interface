from api.schemas.json_formats.ontology import Ontology, OntologyInputType
import strawberry

@strawberry.input
class ComorbidConditionInputType:
    first_typeof: OntologyInputType
    second_typeof_id: OntologyInputType
    second_typeof_label: str
    first_property: str
    schema_id: str
    title: str
    description: str

@strawberry.type
class ComorbidCondition:
    first_typeof: Ontology
    second_typeof: Ontology
    first_property: str
    second_property: str
    schema_id: str
    title: str
    description: str