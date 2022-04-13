from dataclasses import field
from api.schemas.scalars.json_scalar import JSONScalar
from api.interfaces.input import Input
from api.schemas.utils import generic_resolver
from api.schemas.katsu.phenopacket.variant import VariantInputType
from api.schemas.katsu.phenopacket.resource import ResourceInputType
from api.schemas.katsu.phenopacket.procedure import ProcedureInputType
from api.schemas.katsu.phenopacket.phenotypicfeature import PhenotypicFeatureInputType
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket, PhenopacketInputType
from api.schemas.metadata import MetaDataInputType
from api.schemas.katsu.phenopacket.interpretation import InterpretationInputType
from api.schemas.katsu.phenopacket.individual import IndividualInputType
from api.schemas.katsu.phenopacket.htsfile import HtsFileInputType
from api.schemas.katsu.phenopacket.genomicinterpretation import GenomicInterpretationInputType
from api.schemas.katsu.phenopacket.gene import GeneInputType
from api.schemas.katsu.phenopacket.disease import DiseaseInputType
from api.schemas.katsu.phenopacket.diagnosis import DiagnosisInputType
from api.schemas.katsu.phenopacket.biosample import BiosampleInputObjectType
from typing import List, Optional
import strawberry
from sklearn import preprocessing, model_selection, linear_model
import pandas as pd

DEFAULT_LOGREG_RESPONSE = {
    "init_params": {
        "C": None,
        "class_weight": None,
        "dual": None,
        "fit_intercept": None,
        "intercept_scaling": None,
        "l1_ratio": None,
        "max_iter": None,
        "multi_class": None,
        "n_jobs": None,
        "penalty": None,
        "random_state": None,
        "solver": None,
        "tol": None,
        "verbose": None,
        "warm_start": None
    },
    "model_params": {
        "coef_": None,
        "intercept_": None,
        "classes_": None,
        "n_iter_": None
    }
}

@strawberry.input
class AggregateQueryFilter(Input):
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

# TODO: Add other nested object fields as query columns
#       Now we only have subject
@strawberry.input
class PhenopacketQueryColumns(Input):
    column_names: Optional[List[str]] = field(default_factory=list)
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
            res = await generic_resolver_helper(info, "phenopackets_loader", aggregate_filter.phenopacket_filter.ids, None)
        if dependent_variables.__getattribute__("phenopacket") != None:
            named_columns = dependent_variables.phenopacket.column_names + dependent_variables.phenopacket.subject.column_names + ["filter"]
            df = pd.DataFrame(columns = named_columns)
            for phenopacket in res.output:
                phenopacket = Phenopacket.deserialize(phenopacket)
                new_row = dict()
                for name in dependent_variables.phenopacket.column_names:
                    new_row[name] = phenopacket.__getattribute__(name)
                for name in dependent_variables.phenopacket.subject.column_names:
                    new_row[name] = phenopacket.subject.__getattribute__(name)
                new_row["filter"] = Phenopacket.filter(phenopacket, aggregate_filter.phenopacket_filter)
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df = df.apply(preprocessing.LabelEncoder().fit_transform)
            y = df['filter'].copy()
            X = df.drop(['filter'], axis = 1)
            X_train, _, y_train, _ = model_selection.train_test_split(X, y, test_size=0.25, random_state=123)
            model = linear_model.LogisticRegression()
            model.fit(X_train, y_train)
            return logistic_regression_to_dict(model)
        
        # No other response could be formed
        return DEFAULT_LOGREG_RESPONSE

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
            filtered_res = await generic_resolver(info, "phenopackets_loader", aggregate_filter.phenopacket_filter, Phenopacket)
            return len(filtered_res)
        
        # No other response could be formed
        return 0

    @strawberry.field
    async def ratio(self, info, aggregate_filter: AggregateQueryFilter = None) -> float:
        if aggregate_filter.phenopacket_filter != None:
            filtered_res = await generic_resolver(info, "phenopackets_loader", aggregate_filter.phenopacket_filter, Phenopacket)
            all_res = await generic_resolver(info, "phenopackets_loader", None, Phenopacket)

            if len(all_res) != 0:
                return len(filtered_res)/len(all_res)

        # No other response could be formed
        return 0.0