FROM python:3.9

WORKDIR /client

COPY . /client

ENV PORT=3000
EXPOSE 3000

CMD ["python", "-m", "http.server", "3000"]
