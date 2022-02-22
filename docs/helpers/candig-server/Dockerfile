# syntax=docker/dockerfile:1

FROM python:3.6
LABEL Maintainer="CanDIG Project"

ADD . /code
WORKDIR /code

USER root
SHELL ["/bin/bash" , "-c"]
RUN python3 -m pip install --user --upgrade pip
RUN python3 -m pip install --user virtualenv
RUN bash ./build_candig
WORKDIR /code
CMD ["bash", "./start_candig"]
