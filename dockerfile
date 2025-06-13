FROM  python:3.11.13



COPY /home/requirements.txt requirements.txt
WORKDIR /home

RUN apt-get update \
    apt-get install pip \
    pip install -r requirements.txt

EXPOSE 5000
EXPOSE 8000