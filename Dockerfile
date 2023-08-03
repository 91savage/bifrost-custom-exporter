FROM python:3.11-alpine

RUN mkdir -p /app && apk update && apk add gcc libc-dev
WORKDIR /app
COPY metrics /app/metrics
COPY config /app/config
COPY bifrost_metrics.py poetry.lock pyproject.toml README.md ./
RUN pip3 install poetry && poetry config virtualenvs.create false
RUN poetry install --no-dev
CMD ["python3", "bifrost_metrics.py"]


