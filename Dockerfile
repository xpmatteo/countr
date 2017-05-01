FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_APP=countr.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
