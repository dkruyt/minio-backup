# Use the official Python 3.11 image as base.
FROM python:3.11-slim

# Set the working directory in the container.
WORKDIR /usr/src/app

# Copy the script into the container.
COPY backup.py .

# Install any dependencies required by your script here.
# For example, if you need 'requests' uncomment the line with pip install.
RUN pip install --no-cache-dir minio

# Command to run when starting the container.
CMD [ "python", "./backup.py" ]
