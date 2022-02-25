import os

GRAPHQL_BEACON_VERSION = "1.0.0"
GRAPHQL_KATSU_API = os.getenv("GRAPHQL_KATSU_API", "http://graphql-candigv2_tyk_1:8080/katsu/api")
GRAPHQL_CANDIG_SERVER = os.getenv("GRAPHQL_CANDIG_SERVER", "http://graphql-candigv2_tyk_1:8080/candig")
GRAPHQL_BEACON_ID = os.getenv("GRAPHQL_BEACON_ID", "com.candig.graphql-interface")
GRAPHQL_KATSU_TOKEN_KEY = os.getenv("GRAPHQL_KATSU_TOKEN_KEY", "authorization")
GRAPHQL_CANDIG_TOKEN_KEY = os.getenv("GRAPHQL_CANDIG_TOKEN_KEY", "authorization")
