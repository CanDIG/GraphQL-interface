import os

GRAPHQL_KATSU_API = os.getenv("GRAPHQL_KATSU_API", "http://chord-metadata:8008/api")
GRAPHQL_CANDIG_SERVER = os.getenv("GRAPHQL_CANDIG_SERVER", "http://candig-server:3001")
GRAPHQL_BEACON_ID = os.getenv("GRAPHQL_BEACON_ID", "com.candig.graphql-interface")
GRAPHQL_BEACON_VERSION = "1.0.0"
GRAPHQL_KATSU_TOKEN_KEY = os.getenv("GRAPHQL_KATSU_TOKEN_KEY", "X-CANDIG-LOCAL-OIDC")