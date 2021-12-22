### Running

Set up rego development playground
```
git clone https://github.com/CanDIG/rego_development_playground.git
```

Export CANDIG_SERVER and KATSU_API environment variables
For example:
```
export CANDIG_SERVER=http://candig-dev:4000
export KATSU_API=http://localhost:8001/api
```

Install the requirements.txt
```
pip install -r requirements.txt
```

Run the GraphQL interface
``` 
uvicorn app:app --reload --port 7999
```

### How to use GraphQL UI
Use GraphQL UI at http://localhost:7999/graphql

Sample Queries:
```
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
```

View auto-generated Docs on the top right corner of the GraphQL UI

Root Type is query, and top level types under query are katsuDataModels, candigServerVariants and aggregate

## Query Variants on Candig Server
Sample Query:
```
    candigServerVariants(input:{start:"0", end:"10000"})
    {
        variantSetId
        referenceName
        getKatsuIndividuals
        {
            active
            race
    }
  }
```
The `input` follows the same criteria described in Candig Server's documentation for /variants/search https://candig-server.readthedocs.io/en/v1.5.0-alpha/api.html#sample-queries-for-all-variants-services