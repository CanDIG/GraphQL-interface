### Running

Set up rego development playground
```
git clone https://github.com/CanDIG/rego_development_playground.git
```

Export CANDIG_SERVER and KATSU_API environment variables
```
export CANDIG_SERVER=http://candig-dev:4000
export KATSU_API=http://localhost:8001/api
```

Run the GraphQL interface
``` 
uvicorn app:app --reload --port 7999
```