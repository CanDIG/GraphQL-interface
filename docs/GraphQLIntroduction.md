# GraphQL Introduction

GraphQL, as noted on its [website](https://www.graphql.org) is an API query language built to return predictable API data, eliminating the overcollection and undercollection of data that is present in traditional REST APIs.

To be able to run this project in its entirety, there are several steps that one has to take to ensure full compatibility. Note that it is extremely recommended that you build the entire system up with docker, rather than building the components individually.

As a note, some of the documentation and some scripts in this folder have been borrowed from the [federated-learning repository](https://github.com/CanDIG/federated-learning), the [GraphQL-interface repository](https://github.com/CanDIG/GraphQL-interface) and from the [CanDIG Server Documentation](https://candig-server.readthedocs.io/en/v1.5.0-alpha/index.html).

### Context

Each of the Endpoints added to this GraphQL interface provides a useful tool for performing complex API queries.

The GraphQL interface right now only supports Querying, not Mutating, though that could be added in the future.

> Query
>
> - katsuDataModels
>   - Purpose: Access Phenotypic and mCODE Data for Patients with records stored in the Katsu Database
> - candigServerVariants
>   - Purpose: Access Variant Data for patients stored in the CanDIG service
> - aggregate
>   - Purpose: Perform aggregate queries like ML and count queries to gain insights from the patient data stored in the Katsu Database
> - beaconQuery
>   - Purpose: Perform native cross-service queries to get mCODE, phenopacket and patient information for patients with records in the Katsu and canDIG servers.

### Dependencies

1. [CanDIG/Katsu](https://github.com/CanDIG/katsu)
   - This module provides the GraphQL service with a local instance of the Katsu API to get clinical and phenotypic patient data.
   - Clone the CanDIG/Katsu repository into a local directory.
     - As of the 2nd of February, 2022, the latest commit to be verified as working with the GraphQL-interface is the commit `a321c235d52b615aef2cf97393eb20214bed6707` present in the `develop` branch.
   - Once the repository has been cloned up to the specific commit mentioned above, we need to pull submodule updates with the `git submodule update --init` command. Ensure you are in your local `katsu` directory before performing this command.
   - As a whole, these are the commands one will most likely need to perform:
   ```bash
   git clone https://github.com/CanDIG/katsu.git
   cd katsu
   git checkout a321c235d52b615aef2cf97393eb20214bed6707
   git submodule update --init
   ```
2. [Federated-Learning](https://github.com/CanDIG/federated-learning)
   - This module acts as a hub for the full GraphQL setup.
   - Clone the CanDIG/federated-learning repository into a local directory.
     - The main branch's `39c961d7e9e777694edc79d36cea0025cd21e603` commit was verified to be working as of February 2, 2022.
   - Once the repository has been cloned and set to the aforementioned commit, we `cd` into the federated-learning repository and pull its submodule updates with `git submodule update --init`.
   - As a whole, the commands one will most likely need to perform:
   ```bash
   git clone https://github.com/CanDIG/federated-learning.git
   cd federated-learning
   git checkout 39c961d7e9e777694edc79d36cea0025cd21e603
   git submodule update --init
   ```
3. [GraphQL-interface](https://github.com/CanDIG/GraphQL-interface)
   - It goes without saying, but this module provides the heart and soul of the GraphQL interface.
   - Clone the CanDIG/GraphQL-interface repository into a local directory.
     - The latest branch on main should be set up to be used for Katsu and CanDIG work, but as of February 2, 2022, the Beacon Implementation is still under development and as such, will need to be pulled from its specific branch, if working with Beacon.
   - As a whole, the following commands will need to be performed:
   ```bash
   git clone https://github.com/CanDIG/GraphQL-interface.git
   ```
4. [CanDIG-V1 Server](https://candig-server.readthedocs.io/en/v1.5.0-alpha/index.html)
   - This module provides the CanDIG-V1 server for use with the GraphQL variant and Beacon services.
   - It is recommended that you set the server up and collect the data simultaneously, given that both processess are quite long. Hence, we have provided a [Dockerfile](helpers/candig-server/Dockerfile) with which one can create the server and load mock variant data.
   - The server installation will be automatically completed when we load the [docker-compose](helpers/docker-compose.yaml) file

### Environment

For the GraphQL service to run smoothly, we need to be able to set up some environment variables and dependencies.

1. Within the federated-learning repository, copy the default environment file into a local environment file with: `cp .default.env .env`
2. Within the federated-learning repository, modify the `.env` file, modifying the `KATSU_DIR` variable to point to the Katsu directory on your machine. Add two additional variables to the `.env` file, `CANDIG_DIR` and `GRAPHQL_DIR`, and modify their values to point to the respective directories. Note that the CanDIG directory will likely be located within the GraphQL directory (i.e. `GraphQL-interface/docs/helpers/candig-server/`)
3. Replace the `docker-compose.yaml` file in the federated-learning repository with the `docker-compose.yaml` file present in the helpers folder.

### Quick Start

1. Within the federated-learning directory, start up docker with `docker-compose up`. This will start the CanDIG server, the GraphQL interface as well as the Katsu DB.
2. Once the setup for all 3 are complete, ensure the endpoints can be reached:
   - Visit `http://localhost:8000` to ensure the Katsu API is loading up as required
   - Visit `http://localhost:3000` to ensure the CanDIG V1 Server is up and running
   - Visit `http://localhost:7999/graphql` to ensure the GraphQL service is up and running. You should be able to see a GraphiQL UI at this point.

### Data Collection & Ingestion

Only the CanDIG server will have data ingested at this point. For further data ingestion, look to the [GraphQLDataCollection](GraphQLDataCollection.md) file.

### Sample Queries

Examples of Sample Queries can be found in the [GraphQLSampleQueries](GraphQLSampleQueries.md) file