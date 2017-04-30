FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV MYSQL_DATABASE_DB=countr_prod
ENV MYSQL_DATABASE_HOST=
ENV MYSQL_DATABASE_USER=countr
ENV MYSQL_DATABASE_PASSWORD=cheigiyoo2Ooghee
ENV FLASK_APP=countr.py

ENTRYPOINT flask run --host=0.0.0.0

