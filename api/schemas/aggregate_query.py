from api.schemas.scalars.json_scalar import JSONScalar
from api.interfaces.input import Input
from api.schemas.utils import gene_filter, generic_all_resolver
from api.schemas.variant import Variant, VariantInputType
from api.schemas.resource import ResourceInputType
from api.schemas.procedure import ProcedureInputType
from api.schemas.phenotypicfeature import PhenotypicFeatureInputType
from api.schemas.phenopacket import Phenopacket, PhenopacketInputType
from api.schemas.metadata import MetaDataInputType
from api.schemas.interpretation import InterpretationInputType
from api.schemas.individual import IndividualInputType
from api.schemas.htsfile import HtsFileInputType
from api.schemas.genomicinterpretation import GenomicInterpretationInputType
from api.schemas.gene import GeneInputType
from api.schemas.disease import Disease, DiseaseInputType
from api.schemas.diagnosis import DiagnosisInputType
from api.schemas.biosample import BiosampleInputObjectType
from typing import List, Optional
import strawberry
import sklearn as sk
from sklearn import preprocessing, model_selection, linear_model
import pandas as pd
import json
@strawberry.input
class AggregateQueryFilter(Input):
    # filter: Optional[Union[BiosampleInputObjectType, DiagnosisInputType, DiseaseInputType,
    #                 GeneInputType, GenomicInterpretationInputType, HtsFileInputType,
    #                 IndividualInputType, InterpretationInputType, MetaDataInputType, PhenopacketInputType,
    #                 PhenotypicFeatureInputType, ProcedureInputType, ResourceInputType, VariantInputType]] = None
    biosample_filter: Optional[BiosampleInputObjectType] = None
    diagnosis_filter: Optional[DiagnosisInputType] = None
    disease_filter: Optional[DiseaseInputType] = None
    gene_filter: Optional[GeneInputType] = None
    genomic_interpretation_filter: Optional[GenomicInterpretationInputType] = None
    hts_file_filter: Optional[HtsFileInputType] = None
    individual_filter: Optional[IndividualInputType] = None
    interpretation_filter: Optional[InterpretationInputType] = None
    meta_data_filter: Optional[MetaDataInputType] = None
    phenopacket_filter: Optional[PhenopacketInputType] = None
    phenotypic_feature_filter: Optional[PhenotypicFeatureInputType] = None
    procedure_filter: Optional[ProcedureInputType] = None
    resource_filter: Optional[ResourceInputType] = None
    variant_filter: Optional[VariantInputType] = None

@strawberry.input
class IndividualQueryColumns(Input):
    column_names: Optional[List[str]] = None

@strawberry.input
class PhenopacketQueryColumns(Input):
    column_names: Optional[List[str]] = None
    subject: Optional[IndividualQueryColumns] = None


@strawberry.input
class AggregateQueryColumns(Input):
    phenopacket: Optional[PhenopacketQueryColumns] = None

@strawberry.type
class MachineLearningQuery:
    @strawberry.field
    async def logistic_regression(self, info, aggregate_filter: AggregateQueryFilter = None, dependent_variables: AggregateQueryColumns = None) -> JSONScalar:
        res = []
        if aggregate_filter.phenopacket_filter != None:
            res = await generic_all_resolver(info, "phenopacket_loader", aggregate_filter.phenopacket_filter)
        if dependent_variables.__getattribute__("phenopacket") != None:
            named_columns = dependent_variables.phenopacket.subject.column_names + ["filter"]
            df = pd.DataFrame(columns = named_columns)
            for phenopacket in res.output:
                new_row = dict()
                for name in dependent_variables.phenopacket.subject.column_names:
                    new_row[name] = phenopacket.subject.__getattribute__(name)
                    new_row["filter"] = Phenopacket.filter(phenopacket, aggregate_filter.phenopacket_filter)
                df = df.append(new_row, ignore_index=True)
            df = df.apply(preprocessing.LabelEncoder().fit_transform)
            y = df['filter'].copy()
            X = df.drop(['filter'], axis = 1)
            X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25, random_state=123)
            model = linear_model.LogisticRegression()
            model.fit(X_train, y_train)
            return logistic_regression_to_dict(model)

def logistic_regression_to_dict(lrmodel):
    data = {}
    data['init_params'] = lrmodel.get_params()
    data['model_params'] = mp = {}
    for p in ('coef_', 'intercept_','classes_', 'n_iter_'):
        mp[p] = getattr(lrmodel, p).tolist()
    return data

@strawberry.type
class AggregateQuery:
    @strawberry.field
    async def machine_learning(self, info) -> MachineLearningQuery:
        return MachineLearningQuery()
    
    @strawberry.field
    async def count(self, info, aggregate_filter: AggregateQueryFilter = None) -> int:
        if aggregate_filter.phenopacket_filter != None:
            filtered_res = await generic_all_resolver(info, "phenopacket_loader", aggregate_filter.phenopacket_filter, Phenopacket)
            return len(filtered_res)

    @strawberry.field
    async def ratio(self, info, aggregate_filter: AggregateQueryFilter = None) -> float:
        if aggregate_filter.phenopacket_filter != None:
            filtered_res = await generic_all_resolver(info, "phenopacket_loader", aggregate_filter.phenopacket_filter, Phenopacket)
        all_res = await generic_all_resolver(info, "phenopacket_loader", None, Phenopacket)
        return len(filtered_res)/len(all_res)