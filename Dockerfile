FROM python:3.7-slim as base
WORKDIR /artoolbox
ENV PYTHONUNBUFFERED True
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

FROM base as test
COPY test_requirements.txt .
RUN pip install -r test_requirements.txt

FROM base