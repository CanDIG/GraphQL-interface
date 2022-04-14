from api.schemas.aggregate.aggregate_classes import DEFAULT_LOGREG_RESPONSE, AggregateQueryFilter, AggregateQueryColumns
from api.schemas.katsu.phenopacket.phenopacket import Phenopacket
from sklearn import preprocessing, model_selection, linear_model
from api.schemas.scalars.json_scalar import JSONScalar
from api.schemas.utils import generic_resolver_helper
import pandas as pd
import strawberry

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