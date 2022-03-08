'''
Purpose:
  Script depicting a sample query in GraphQL, along with its time to completion, to contrast traditional 
  REST APIs to GraphQL APIs.
'''

import requests
import time
import json

GRAPHQL_ENDPOINT = 'http://localhost:7999'
DEFAULT_QUERY = '''
query {
  beaconQuery(input:{
    referenceName: "1",
    referenceBases: "T",
    alternateBases: "C",
    start: 712800,
    end: 712900
  }){individualsPresent{
    personalInfo{dateOfBirth}
  }}
}
'''


if __name__ == "__main__":
    t1 = time.time()
    response = requests.post(GRAPHQL_ENDPOINT, json={'query': DEFAULT_QUERY})
    individuals = json.loads(response.text)['data']['beaconQuery']['individualsPresent']
    print([individual['personalInfo']['dateOfBirth'] for individual in individuals])
    print(f'Execution took: {time.time() - t1}s')