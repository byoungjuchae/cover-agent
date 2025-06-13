FROM  python:3.11.13

WORKDIR /home

COPY requirements.txt .

RUN apt-get update \
    apt-get install pip \
    pip install -r requirements.txt --no-cache-dir

EXPOSE 5000
EXPOSE 8000