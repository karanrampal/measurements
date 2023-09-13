FROM python:3.8-slim

WORKDIR /measurement

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

COPY ./src .

CMD uvicorn --port $PORT --host 0.0.0.0 main:app
