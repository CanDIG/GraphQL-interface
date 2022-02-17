# syntax=docker/dockerfile:1

ARG GRAPHQL_CONDA_SOURCE=condaforge
ARG GRAPHQL_CONDA_TYPE=miniforge3
ARG GRAPHQL_CONDA_VERSION=latest

FROM ${GRAPHQL_CONDA_SOURCE}/${GRAPHQL_CONDA_TYPE}:${GRAPHQL_CONDA_VERSION}

LABEL Maintainer="CanDIG Project"

COPY . /app/GraphQL-interface

WORKDIR /app/GraphQL-interface

USER root

RUN apt update

RUN apt install gcc musl-dev -y \
	&& conda install --file conda-requirements.txt \
    && pip install -U setuptools pip \
    && pip install -r requirements.txt
	
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7999", "--proxy-headers"]
