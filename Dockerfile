# syntax=docker/dockerfile:1
FROM python:3.9-alpine3.13
ADD . /code
WORKDIR /code

LABEL Maintainer="CanDIG Project"

USER root

RUN apk update

RUN apk add --no-cache \
	autoconf \
	automake \
	bash \
	build-base \
	bzip2-dev \
	cargo \
	curl \
	curl-dev \
	gcc \
	git \
	libcurl \
	libffi-dev \
	libressl-dev \
	linux-headers \
	make \
	musl-dev \
	perl \
	postgresql-dev \
	postgresql-libs \
	xz-dev \
	yaml-dev \
	zlib-dev
RUN apk add --no-cache --virtual .build-deps gcc musl-dev build-base \
    && pip install -U setuptools pip \
    && pip install -r requirements.txt \
    && apk del .build-deps
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7999"]
