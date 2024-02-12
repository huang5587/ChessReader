FROM python:3.9

RUN apt-get update && apt-get install -y \
    pychess \
    stockfish \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "-u", "server.py"]


