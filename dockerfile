FROM ollama/ollama:0.1v

RUN pip install -r requirements.txt

WORKDIR /home

COPY . .

