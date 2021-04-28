FROM python:3.8-slim-buster

RUN \
    apt-get update &&\
    apt-get install -y --no-install-recommends tini && \
    pip install -U pip &&\
    pip install poetry &&\
    poetry config virtualenvs.create false

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .

ENV PYTHONPATH=.

EXPOSE 8080

USER nobody

ENTRYPOINT ["tini", "--"]
