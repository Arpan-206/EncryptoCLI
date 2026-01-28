FROM python:3.14-alpine
RUN apk add build-base libffi-dev
RUN pip install uv
WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY . .
RUN uv sync --frozen 