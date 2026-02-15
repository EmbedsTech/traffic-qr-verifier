# Use a stable Python version
FROM python:3.11-slim

# Install system dependencies with updated package names
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Set the port Render expects
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
