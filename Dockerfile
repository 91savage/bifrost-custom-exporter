FROM python:3.11-alpine

RUN mkdir -p /app && apk update && apk add gcc libc-dev
WORKDIR /app
COPY metrics /app/metrics
COPY bifrost_metrics.py poetry.lock pyproject.toml README.md /app/
RUN pip3 install poetry && poetry config virtualenvs.create false
RUN poetry install --no-dev
CMD ["python3", "bifrost_metrics.py"]


