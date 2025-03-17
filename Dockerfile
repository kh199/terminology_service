FROM python:3.11-alpine

RUN mkdir /app

COPY pyproject.toml /app

WORKDIR /app

RUN apk add --no-cache curl \
    && pip install --upgrade pip \
    && pip install poetry --no-cache-dir \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --without dev

COPY src/ /app

CMD ["gunicorn", "src.wsgi:application", "--bind", "0:8000" ] 
