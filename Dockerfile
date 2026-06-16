FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir uv
RUN uv sync --no-dev

COPY . .

ENTRYPOINT ["uv", "run", "python", "-m", "src.main"]
