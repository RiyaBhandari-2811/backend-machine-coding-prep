# Dockerfile - Machine Learning Application Example
# Example: Laptop Price Predictor with Streamlit

FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/

# Install dependencies including system-level packages if needed
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED=1

# Streamlit-specific configurations
# Tell Streamlit to run in headless mode (no browser)
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "enableCORS = false" >> ~/.streamlit/config.toml

# Expose Streamlit default port
EXPOSE 8501

# Important: Make sure Flask/Streamlit listens on 0.0.0.0
# This allows access from outside the container
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]

# ============================================================================
# WHY PYTHON 3.8?
# This ML project might have been built with Python 3.8
# Using same version ensures library compatibility
#
# WHY NO FULL OS?
# -slim variant: ~150MB vs full ~900MB
# Contains only essential packages for running Python
#
# HOW TO BUILD:
# docker build -t yourusername/laptop-predictor:1.0 -f Dockerfile.ml .
#
# HOW TO RUN:
# docker run -p 8501:8501 yourusername/laptop-predictor:1.0
# Visit: http://localhost:8501
#
# WHY EXPOSE 8501?
# That's Streamlit's default port
#
# ============================================================================
