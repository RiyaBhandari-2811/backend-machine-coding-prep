# Stage 1: Build image for our FastAPI application
# This Dockerfile is designed for the Insurance Premium Prediction API from Chapter 7

# Use lightweight Python base image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file first (better caching)
COPY requirements.txt .

# Install dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire application code
COPY . .

# Prevent Python output buffering for real-time logs
ENV PYTHONUNBUFFERED=1

# Expose the port where FastAPI will run
EXPOSE 8000

# Run the FastAPI application using uvicorn
# 0.0.0.0 allows connections from any IP (essential for Docker)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
