import pandas as pd
from pymongo import MongoClient
import docker
import json

def get_container_ip(name):
    client = docker.from_env()
    container = client.containers.get(name)  # Replace "cassandraNode" with your actual container name
    container_info = container.attrs
    network_settings = container_info['NetworkSettings']
    container_ip = network_settings['Networks']['ias_project_default']['IPAddress']
    return container_ip
# Create a MongoDB client with authentication details in the connection string
#client = MongoClient('mongodb://admin:password@127.0.0.1:27017/')
with open("./mongo_config.json", "r") as config_file:
    mongo_config = json.load(config_file)
client = MongoClient(
    host=mongo_config["mongo_host"],
    port=mongo_config["mongo_port"],
    username=mongo_config["mongo_username"],
    password=mongo_config["mongo_password"],
    authSource='admin'
)
# Get the database
db = client['ias']

# Create a collection (if it doesn't already exist)
collection_name = 'ias_overview'  # Replace with your collection name
collection = db.get_collection(collection_name)
if collection is None:
    db.create_collection(collection_name)

# Load CSV data into a DataFrame
df = pd.read_csv('./dataset.csv')  # Replace with your CSV file path

# Convert DataFrame to a list of dictionaries (JSON-like objects)
data = df.to_dict(orient='records')

# Insert data into MongoDB
collection.insert_many(data)
print("Datas inserted!")
# Close the MongoDB connection
client.close()
