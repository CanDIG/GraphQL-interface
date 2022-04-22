# syntax=docker/dockerfile:1

ARG GRAPHQL_PYTHON_VERSION=3.8

FROM python:${GRAPHQL_PYTHON_VERSION}-slim

LABEL Maintainer="CanDIG Project"

COPY . /app/GraphQL-interface

WORKDIR /app/GraphQL-interface

USER root

RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7999", "--proxy-headers"]
