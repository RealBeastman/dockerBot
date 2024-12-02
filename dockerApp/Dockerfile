# Use a base image with Python
FROM python:3.10

# Set the working directory
WORKDIR /app

# Find and copy the dockerBot package
COPY ./dockerBotPackage /app/dockerBot

# Install dockerBot
RUN pip install git+https://github.com/RealBeastman/relay_service.py.git@main

# Copy the Docker app script
COPY client.py /app/

# Run the Docker app when the container starts
CMD ["python", "client.py"]