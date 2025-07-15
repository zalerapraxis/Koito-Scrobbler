# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y procps curl && rm -rf /var/lib/apt/lists/*

# Run koito-scrobbler-service.py when the container launches
# Declare a volume for the Spotify .cache file
VOLUME ["/app/.cache"]

CMD ["python", "koito-scrobbler-service.py"]

ADD healthcheck.sh /usr/local/bin/healthcheck.sh
RUN chmod +x /usr/local/bin/healthcheck.sh
# Health check to ensure the script is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 CMD ["/usr/local/bin/healthcheck.sh"]