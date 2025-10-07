# ======================
# 1. Builder stage
# ======================
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry self add poetry-plugin-export

COPY pyproject.toml poetry.lock /app/

# Export requirements and install dependencies
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && find /install -type f -name '*.pyc' -delete

# ======================
# 2. Runtime stage
# ======================
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY src /app/src

EXPOSE 8443

# Set environment variables (prefer Docker secrets or env vars over .env in production)
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
ENV BASE_URL=${BASE_URL}

# Run the bot with the correct path
CMD ["python", "-m", "src.main"]