# syntax=docker/dockerfile:1

ARG GRAPHQL_PYTHON_VERSION=3.8

FROM python:${GRAPHQL_PYTHON_VERSION}-slim

LABEL Maintainer="CanDIG Project"

COPY . /app/server

WORKDIR /app/server

USER root

RUN pip install uvicorn==0.16.0 fastapi==0.71.0
	
CMD ["uvicorn", "server:server", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]