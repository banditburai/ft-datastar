# Use official Python image
FROM python:3.11-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

ARG APP_VERSION=dev
RUN if [ -f version.py ]; then \
        echo "Using existing version.py"; \
    else \
        echo "__version__ = '${APP_VERSION}'" > version.py; \
    fi
    
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up app directory
WORKDIR /app

# Copy the rest of the application
COPY . .

# Expose port and run application
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]