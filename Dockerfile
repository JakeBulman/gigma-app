#Python Docker Image
FROM python:3.12

RUN apt-get update && \
    apt-get install -y
RUN pip install --upgrade pip
RUN pip install uwsgi

#Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PGSSLCERT /tmp/postgresql.crt

RUN mkdir /code
WORKDIR /code
COPY . /code

#Install dependencies

COPY requirements.txt /code/
RUN pip install -r requirements.txt