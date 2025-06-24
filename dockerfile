FROM python:3.11.12-alpine

WORKDIR /home

COPY . .

COPY requirements.txt /home/requirements.txt

RUN pip install -r requirements.txt