# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Copy code and install deps
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["python", "main.py"]
