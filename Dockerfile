FROM python:3.12.0a4-alpine
RUN apk add build-base libffi-dev
RUN pip3 install --no-cache --upgrade pip setuptools 
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install --no-cache -r requirements.txt