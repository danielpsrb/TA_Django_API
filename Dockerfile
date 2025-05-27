# Use python 3.10
FROM python:3.10-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1 

# Copy the entire current directory (.) into the /app directory in the container
COPY . /app/

# Install dependencies first for caching benefit
RUN pip install --upgrade pip 
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt