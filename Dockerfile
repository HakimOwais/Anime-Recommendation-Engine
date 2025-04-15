FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install numpy first with specific version
RUN pip install numpy==1.19.2 --no-cache-dir

# Then install other dependencies
RUN pip install --no-cache-dir -e . && \
    pip uninstall -y tensorflow && \
    pip install tensorflow==2.12.0 --no-cache-dir

# Run the training pipeline
RUN python pipeline/training_pipeline.py

EXPOSE 8000
CMD ["python", "application/api.py"]