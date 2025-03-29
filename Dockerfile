# Use python 3.10
FROM python:3.10.16-slim AS builder

# Set an environment variable to unbuffer Python output, aiding in logging and debugging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Define an environment variable for the web service's port, commonly used in cloud services
ENV PORT 8080

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the entire current directory (.) into the /app directory in the container
COPY . /app/

# Install dependencies first for caching benefit
RUN pip install --upgrade pip 
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt