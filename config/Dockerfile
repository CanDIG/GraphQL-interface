# syntax=docker/dockerfile:1

ARG conda_source
ARG conda_type
ARG conda_version

FROM ${conda_source}/${conda_type}:${conda_version}

LABEL Maintainer="CanDIG Project"

COPY . /app/GraphQL-interface

WORKDIR /app/GraphQL-interface

USER root

RUN apt update

RUN apt install gcc musl-dev -y \
	&& conda install --file conda-requirements.txt \
    && pip install -U setuptools pip \
    && pip install -r requirements.txt
	
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7999"]
