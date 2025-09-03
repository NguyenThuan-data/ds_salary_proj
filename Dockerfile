# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=3000 \
    PIP_NO_CACHE_DIR=1

# System deps (none needed beyond base for this simple app)
WORKDIR /app

# Install deps first for better caching
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy app source
COPY . .

EXPOSE 3000

# Use gunicorn in production
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-3000} --workers 2 --timeout 120"]
