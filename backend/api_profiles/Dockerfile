# syntax=docker/dockerfile:1

FROM python:3-slim
WORKDIR /programas/api-games

COPY request.txt request.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

run pip3 install -r request.txt

COPY . .

CMD [ "python3", "./app.py" ]
