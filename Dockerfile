# 🏦 BlackRock Ultra Screener - Docker
# Usage: docker build -t screener . && docker run -it screener

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY stock_screener_ultra_v10.py .
COPY telegram_bot.py .
COPY screener_config_v10.json .
COPY .env.example .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV TELEGRAM_BOT_TOKEN=""

# Default: run the bot (headless mode)
# For GUI, use: docker run -it screener python stock_screener_ultra_v10.py
CMD ["python", "telegram_bot.py"]
