# Use the official Python slim image for a smaller footprint
FROM python:3.10-slim

# Set environment variables for consistent behavior
ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# Set the working directory
WORKDIR /app

# Install system dependencies (ffmpeg is needed for media processing)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "wisp.py"]
