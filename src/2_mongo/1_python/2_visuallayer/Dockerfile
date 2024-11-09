# Use an official Python runtime as a parent image
FROM python:3.8-slim

RUN apt-get -y update

RUN pip install --upgrade pip

# Set the working directory to /app
WORKDIR /usr/src/app

RUN mkdir /usr/src/my_share

RUN mkdir /usr/src/get_module

# Make port 8888 available to the world outside this container
EXPOSE 8888 5000 443 27017 80 9042

# Copy the current directory contents into the container at /app
#COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Run app.py when the container launches
CMD ["python3", "Queryform.py"]

