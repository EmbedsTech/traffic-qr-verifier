FROM python:3.11-slim

# Install the missing zbar library and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render expects the app to listen on port 10000 by default for Docker
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
