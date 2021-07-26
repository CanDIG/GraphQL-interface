import strawberry

@strawberry.input
class OntologyInputType:
    id: str
    label: str

@strawberry.type
class Ontology:
    id: str
    label: str

@strawberry.input
class SampleTissueInputType:
    reference: str
    display: str

@strawberry.type
class SampleTissue:
    reference: str
    display: str

def filter_ontology(instance, input: OntologyInputType):
    id = input.get("id")
    label = input.get("label")
    if id == None and label == None:
        return True
    if id == None:
        return instance.label == label
    if label == None:
        return instance.id == id
    return instance.id == id and instance.label == label