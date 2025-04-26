# app/Dockerfile

FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y gcc netcat

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

COPY entrypoint.sh /app/entrypoint.sh
# Ensure entrypoint.sh has Unix line endings (in case it came from Windows)
RUN sed -i 's/\r$//g' /app/entrypoint.sh

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh
