# syntax=docker/dockerfile:1
FROM condaforge/miniforge3:latest
ADD . /code
WORKDIR /code

LABEL Maintainer="CanDIG Project"

USER root

RUN apt update

RUN apt install gcc musl-dev -y \
	&& conda install --file conda-requirements.txt \
    && pip install -U setuptools pip \
    && pip install -r requirements.txt
	
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7999"]
