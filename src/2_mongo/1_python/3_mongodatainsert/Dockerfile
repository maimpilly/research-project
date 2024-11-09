# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy your Python script and CSV file into the container at /app
COPY . /app/


# Install the required packages
RUN pip install pandas pymongo docker 

# Run your Python script to insert data into MongoDB
CMD ["python", "insertdatatomongo.py"]

