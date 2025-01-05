# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app
# Comment


# Copy the application code into the container
COPY . .

# Install system dependencies and Python dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    gcc \
#    libpq-dev \
#    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask
# Expose Flask's default port (5000)
EXPOSE 5002


ENV FLASK_APP=run.py
# Specify the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]
