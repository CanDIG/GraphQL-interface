## Dependencies
1. **Clone CanDIG/Katsu** The current release of CanDIG/Katsu does not support MCODE data, so you will have to supply a locally built Docker image of CanDIG/Katsu.Clone the [Katsu repository](https://github.com/CanDIG/katsu) to prepare the build context.
2. **Pull submodule updates.** The `federated-learning` repository relies on the `mohccn-data` submodule to provide adequate synthetic data for training purposes. Pull its most recent updates with the following two commands:
- Navigate to the `katsu` repo and run `git submodule update --init`

## Running

If you desire to query Kastu, export the KATSU_API env variable to the URL of your local Katsu instance's API. Ex. `export KATSU_API=http://localhost:8001/api`

If you desire to query the CanDIG server (ex. for cross-service queries), export the CANDIG_SERVER env variable to the URL of the CanDIG server. Ex. `export CANDIG_SERVER=http://candig-dev:4000`

Install the requirements.txt
```
pip install -r requirements.txt
```

Run the GraphQL interface
``` 
uvicorn app:app --reload --port 7999
```

## How to use GraphQL UI
Use GraphQL UI at http://localhost:7999/graphql

Sample Queries:
```
query
{
    katsuDataModels
    {
        mcodeDataModels
        {
            cancerConditions
            {
                id
                bodySite{
                    id
                    label
                }
            }
        }
    }
}
```

View auto-generated Docs on the top right corner of the GraphQL UI

Root Type is query, and top level types under query are katsuDataModels, candigServerVariants and aggregate