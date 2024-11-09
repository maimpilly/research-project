# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy your Python scripts and requirements.txt into the container at /app
COPY . /app/

# Install the required packages
RUN pip install pandas pymongo cassandra-driver docker

# Command to run the script to insert data from MongoDB to Cassandra
CMD ["python", "mongo2cassandra.py"]

