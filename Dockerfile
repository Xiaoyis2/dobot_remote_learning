# Use a Python base image optimized for ARM
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command to run the program
CMD ["python", "main.py"]
