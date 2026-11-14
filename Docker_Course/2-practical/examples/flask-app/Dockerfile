# Dockerfile - Flask Application Example

# Stage 1: Base image with Python
# Using specific version (3.9) for consistency
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file
# This is done before copying the entire app to leverage Docker layer caching
COPY requirements.txt /app/

# Install dependencies
# -r flag reads from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire application code
COPY . /app/

# Set environment variable
# Forces Python to run in unbuffered mode (prints immediately to logs)
ENV PYTHONUNBUFFERED=1

# Expose port
# Application will listen on port 5000 inside container
EXPOSE 5000

# Health check (optional but recommended)
# Periodically check if application is healthy
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Default command when container starts
# Make sure Flask app runs on 0.0.0.0 (accessible from outside container)
CMD ["python", "app.py"]

# ============================================================================
# HOW TO BUILD:
# docker build -t yourusername/flask-app:1.0 .
#
# HOW TO RUN:
# docker run -p 8000:5000 yourusername/flask-app:1.0
# Then visit: http://localhost:8000
#
# HOW TO PUSH:
# docker login
# docker push yourusername/flask-app:1.0
#
# HOW TO PULL (from registry):
# docker pull yourusername/flask-app:1.0
# ============================================================================
