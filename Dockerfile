FROM python:3.8

EXPOSE 443

RUN apt-get update -y && apt-get install -y libpq-dev postgresql-client

WORKDIR /passman_server

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

CMD ./start.sh