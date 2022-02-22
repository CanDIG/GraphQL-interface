# GraphQL-interface Documentation

This module deals with the GraphQL API endpoint and to get it set up, there are attached Markdown Documents that will guide you through the setup process. If you are starting from scratch, then you should follow the order in which objects are listed below, to ensure a quick and easy setup process.

## GraphQL Endpoint Setup

The [following page](GraphQLIntroduction.md) is a guide on setting up the GraphQL service along with its many dependencies onto your local machine.

## GraphQL Data Collection & Ingestion

The [following page](GraphQLDataCollection.md) is a guide to collecting and installing data into the Katsu and CanDIG dependencies for testing and miscellaneous purposes.

## GraphQL Sample Queries

The [following page](GraphQLSampleQueries.md) is a guide to the types of queries one can perform with GraphQL, and specifically the queries one can perform on this GraphQL endpoint. It discusses query building and shows example queries for testing purposes.

## Helper Files

The [following directory](helpers/) contains the modules required for data ingestion into both the Katsu and CanDIG servers. It also has a docker-compose file with which one can setup the entire service with a simple `docker-compose up` command.

## Sample Queries Sub-Directory

The [following directory](samplequeries/) contains scripts detailing how to query GraphQL using python. A sample REST query page is also included to contrast the two data collection strategies. It also contains a comprehensive Beacon Test Script which tests every possible field returnable in a Beacon Request.
