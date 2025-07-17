# Base Python image
FROM python:3.10-slim

# Install poppler-utils and OCR tools
RUN apt-get update && apt-get install -y \
    poppler-utils tesseract-ocr \
    && apt-get clean

# Set working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app

# Set environment variable for Streamlit secrets
ENV STREAMLIT_SECRETS_PATH=/app/interface/.streamlit/secrets.toml

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Streamlit listens on port 8501
EXPOSE 8501

# Run your Streamlit app (note: correct relative path)
CMD ["streamlit", "run", "interface/app.py", "--server.port=8501", "--server.enableCORS=false", "--server.headless=true"]
