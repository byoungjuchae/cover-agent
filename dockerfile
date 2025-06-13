FROM  python:3.11.13

WORKDIR /home

COPY . .

RUN apt-get update \
    apt-get install pip \
    pip install -r requirements.txt

EXPOSE 5000
EXPOSE 8000