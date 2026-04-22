# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependency file first (for better caching)
COPY requirements.txt .

# Install dependencies (DB drivers + LangChain)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy your FastAPI project files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Default command to start your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
