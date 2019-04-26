# pull official base image
FROM python:3.7-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/jengu

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/jengu/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/jengu/entrypoint.sh

# copy project
COPY . /usr/src/jengu/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/jengu/entrypoint.sh"]