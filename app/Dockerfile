FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/app/

COPY ./app/requirements.txt .

RUN useradd -U app && mkdir -p /app && chown -R app:app /app

RUN pip install -r ./requirements.txt

COPY ./app/ .

ENV PYTHONPATH "${PYTHONPATH}:/app/"