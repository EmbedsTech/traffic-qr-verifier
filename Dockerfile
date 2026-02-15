# Use Python 3.14 (matches your Render log)
FROM python:3.14-slim

# Install system dependencies (zbar and opencv requirements)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Command to run the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
