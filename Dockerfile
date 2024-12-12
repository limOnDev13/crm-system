FROM python:3.12

WORKDIR /crm

ENV PYTHONPATHBUFFERED = 1

RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . .
