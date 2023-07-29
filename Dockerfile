# Stage 1: Building FastAPI with 
FROM python:slim

# Copy FastAPI application source code
COPY . /app
WORKDIR /app

# Stage 2: Final image with Python and FastAPI

# Install Python dependencies
RUN apt-get update && apt-get install -y fpc

RUN pip install --no-cache-dir -r requirements.txt

