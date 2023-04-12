FROM python:3.8-slim

WORKDIR /measurement

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src .

ENTRYPOINT ["main"]