FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY . /app

# Add system dependencies for building wheels
RUN apt-get update && apt-get install -y build-essential python3-dev

# Upgrade pip
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
