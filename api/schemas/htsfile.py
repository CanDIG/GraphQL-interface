from api.schemas.scalars.json_scalar import JSONScalar
import strawberry

@strawberry.input
class HtsFileInputType:
    uri: id
    description: str
    hts_format: str
    genome_assembly: str
    individual_to_sample_identifiers: JSONScalar

class HtsFile:
    uri: id
    description: str
    hts_format: str
    genome_assembly: str
    individual_to_sample_identifiers: JSONScalar
    extra_properties: JSONScalar
    created: str
    updated: str

    @strawberry.field
    def individual_to_sample_identifiers(self, info) -> JSONScalar:
        return self.individual_to_sample_identifiers
    
    @strawberry.field
    def extra_properties(self, info) -> JSONScalar:
        return self.extra_properties