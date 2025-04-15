# Use a lightweight Python image as the Base Image
FROM python:3.8-slim

# Setting up env variables 
# - PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files (cached bytecode files)
# - PYTHONUNBUFFERED=1 ensures that Python output is displayed immediately (useful for logging)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by TensorFlow
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setting working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies from the project's setup file (editable mode)
RUN pip install --no-cache-dir -e .

# Run the training pipeline before starting the application
RUN python pipeline/training_pipeline.py

# Expose port 8000 to allow external access to the application
EXPOSE 8000

# Set the default command to run the application API
CMD ["python", "application/api.py"]
