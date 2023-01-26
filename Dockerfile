# syntax=docker/dockerfile:1
FROM python:3.10-alpine
RUN apk update \
    && apk add sqlite \
    && apk add bash

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["bin/httpsserverrun"]
EXPOSE 5050
