from api.schemas.aggregate.aggregate_classes import AggregateQueryFilter, AggregateQueryColumns
from api.schemas.aggregate.defaults import DEFAULT_LOGREG_RESPONSE, PHENOPACKET_COLUMNS
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
            named_column_tuples = get_named_columns(dependent_variables.phenopacket, PHENOPACKET_COLUMNS)
            named_columns = [name[1] for name in named_column_tuples]
            named_columns = [sub_column for column in named_columns for sub_column in column]
            named_columns = named_columns + dependent_variables.phenopacket.column_names + ["filter"]
            df = pd.DataFrame(columns = named_columns)
            for phenopacket in res.output:
                phenopacket = Phenopacket.deserialize(phenopacket)
                new_row = dict()
                for name in dependent_variables.phenopacket.column_names:
                    new_row[name] = phenopacket.__getattribute__(name)
                for name in dependent_variables.phenopacket.subject.column_names:
                    new_row[name] = phenopacket.subject.__getattribute__(name)
                for name in dependent_variables.phenopacket.phenotypic_features.column_names:
                    elements = [packet.__getattribute__(name) for packet in phenopacket.phenotypic_features]
                    new_row[name] = max(set(elements), key=elements.count)
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

def get_named_columns(dependent_variables, columns):
    column_names = list()
    for field in columns:
        try:
            field_value = getattr(dependent_variables, field)
        except:
            field_value = False
        
        if field_value:
            column_names.extend([(field, field_value.column_names)])
    
    return column_names