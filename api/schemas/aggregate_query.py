from dataclasses import field
from api.schemas.scalars.json_scalar import JSONScalar
from api.interfaces.input import Input
from api.schemas.utils import generic_resolver, candig_filter
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
from api.schemas.katsu.mcode.mcode_packet import MCodePacketInputType, MCodePacket
from api.schemas.candig_server.variant import CandigServerVariantInput, CandigServerVariant, CandigServerVariantDataLoaderInput
from api.schemas.beacon.beacon_data_models import BeaconAlleleRequest, BeaconAlleleResponse
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
    phenopacket_filter: Optional[PhenopacketInputType] = None
    mcodepacket_filter: Optional[MCodePacketInputType] = None
    variant_filter: Optional[CandigServerVariantInput] = None
    # beacon_filter: Optional[BeaconAlleleRequest] = None 
        # TODO: Add Features related to this when we fully integrate v2 spec

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
        elif aggregate_filter.mcodepacket_filter != None:
            filtered_res = await generic_resolver(info, "mcode_packets_loader", aggregate_filter.mcodepacket_filter, MCodePacket)
            return len(filtered_res)
        elif aggregate_filter.variant_filter != None:
            patient = aggregate_filter.variant_filter.katsu_individual
            patient_ids = patient.ids if patient is not None else [None]
            patient_ids = [None] if patient_ids is None else patient_ids

            ret = []
            for patient_id in patient_ids:
                ret.extend(await info.context["candig_server_variants_loader"].load(CandigServerVariantDataLoaderInput(None, aggregate_filter.variant_filter, patient_id, info)))
            
            individuals = []
            for variant in ret:
                if str(type(variant.get_katsu_individuals)) == "<class 'method'>":
                    individuals.append(await variant.get_katsu_individuals(info))
                else:
                    individuals.append(variant.get_katsu_individuals)
            
            for i in range(len(ret)):
                ret[i].get_katsu_individuals = individuals[i]
            
            ret = [variant for variant in ret if candig_filter(variant, aggregate_filter.variant_filter)]
            
            return len(ret)
        
        # No other response could be formed
        return 0

    @strawberry.field
    async def ratio(self, info, aggregate_filter: AggregateQueryFilter = None) -> float:
        if aggregate_filter.phenopacket_filter != None:
            filtered_len = await self.count(info, aggregate_filter)
            total_len = await self.count(info, AggregateQueryFilter(phenopacket_filter=PhenopacketInputType()))

            if total_len != 0:
                return filtered_len / total_len
        elif aggregate_filter.mcodepacket_filter != None:
            filtered_len = await self.count(info, aggregate_filter)
            total_len = await self.count(info, AggregateQueryFilter(mcodepacket_filter=MCodePacketInputType()))

            if total_len != 0:
                return filtered_len / total_len
        elif aggregate_filter.variant_filter != None:
            filtered_len = await self.count(info, aggregate_filter)
            total_len = await self.count(
                info, AggregateQueryFilter(
                    variant_filter=CandigServerVariantInput(
                        start=aggregate_filter.variant_filter.start, 
                        end=aggregate_filter.variant_filter.end, 
                        referenceName=aggregate_filter.variant_filter.referenceName
                    )
                )
            )

            if total_len != 0:
                return filtered_len / total_len

        # No other response could be formed
        return 0.0