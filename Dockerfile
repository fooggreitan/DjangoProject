#FROM python:3-alpine
#
#WORKDIR /app
#
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
#COPY . .
#
#RUN pip install --upgrade pip
#COPY requirements.txt .
#
#RUN \
# apk add --no-cache python3 postgresql-libs && \
# apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
# python3 -m pip install -r requirements.txt --no-cache-dir && \
# apk --purge del .build-deps

FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
ADD  . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt