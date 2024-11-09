import pandas as pd
from pymongo import MongoClient
from cassandra.cluster import Cluster
import json
import logging
import docker


# Configure logging
logging.basicConfig(level=logging.INFO, filename="mongo2casandra.log")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 1)

db_prefix = ("IAS", "ias")

def get_container_ip(name):
    client = docker.from_env()
    container = client.containers.get(name)  # Replace "cassandraNode" with your actual container name
    container_info = container.attrs
    network_settings = container_info['NetworkSettings']
    container_ip = network_settings['Networks']['ias_project_default']['IPAddress']
    return container_ip

# Function to get connection details for databases with names starting with "ias"
def get_db_connection_details(client):
    database_names = client.list_database_names()
    db_connection_details = []
    for db_name in database_names:
        if db_name.startswith(db_prefix):
            db = client[db_name]
            collections = db.list_collection_names()
            db_connection_details.append({
                "Database Name": db_name,
                "Collections": collections,
                "Connection Details": {
                    "Host": client.address[0],
                    "Port": client.address[1],
                    "username": mongo_config["mongo_username"],  # Use the username from your configuration
                    "password": mongo_config["mongo_password"]},  # Use the password from your configuration
                "get method": "DatabaseData"
            })
    #print(db_connection_details)
    return pd.DataFrame(db_connection_details)

# Function to fetch and display database name, collection name, ID, and timestamp
def fetch_and_insert_data(client, session):
    dfs_to_insert = []
    try:
        for db_name in client.list_database_names():
            if db_name.startswith(db_prefix):
                db = client[db_name]
                for collection_name in db.list_collection_names():
                    data = list(db[collection_name].find())
                    if data:
                        for document in data:
                            #document["_id"] = str(document.get("_id"))  # Convert ObjectId to string
                            #timestamp = str(document.get("timestamp", ""))  # Convert timestamp to string
                            id = str(document.get("ID", ""))
                            condition = str(document.get("Condition", ""))
                            gate_length = str(document.get("Gate_length(L_g)", ""))
                            voltage_gate_source = str(document.get("Voltage_Gate_Source(V_gs)", ""))
                            voltage_drain_source = str(document.get("Voltage_Drain_Source(V_ds)", ""))
                            dfs_to_insert.append({
                                "Collection Name": collection_name,
                                "ID": id,
                                "Condition": condition,
                                "Gate Length": gate_length,
                                "Voltage Gate Source": voltage_gate_source,
                                "Voltage Drain Source": voltage_drain_source
                            })
                            #print(dfs_to_insert)
    except Exception as e:
        logging.error(f"Error fetching data from MongoDB: {e}")
        return []
    # Insert data into data_in_db table
    try:
        for data_entry in dfs_to_insert:
            session.execute("""
                INSERT INTO data_in_db (collection_name, ID, condition, gate_length, voltage_gate_source, voltage_drain_source)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                data_entry['Collection Name'],
                data_entry['ID'],
                data_entry.get('Condition', ''),  # Assuming these fields may not always exist in the MongoDB documents
                data_entry.get('Gate Length', ''),
                data_entry.get('Voltage Gate Source', ''),
                data_entry.get('Voltage Drain Source', '')
            ))
    except Exception as e:
        logging.error(f"Error inserting data into Cassandra: {e}")
        return []
# if dfs_to_insert:
#     result_df = pd.DataFrame(dfs_to_insert)
#     print("Database Name, Collection Name, ID, Timestamp:")
#     print(result_df)
# else:
#     print("No data found.")

# Read MongoDB connection details from a JSON file
with open("./mongo_config.json", "r") as config_file:
    mongo_config = json.load(config_file)

#Establish a MongoDB connection with authentication
client = MongoClient(
    host=get_container_ip('mongodb'),
    port=mongo_config["mongo_port"],
    username=mongo_config["mongo_username"],
    password=mongo_config["mongo_password"],
    authSource='admin'
)


cassandra_host = get_container_ip('cassandraNode')#'cassandraNode'  # Replace with your Cassandra node hostname or IP
#cassandra_host = '172.28.0.3'
cassandra_port = 9042  # Replace with your Cassandra port

cluster = Cluster([cassandra_host], port=cassandra_port)
session = cluster.connect()

# Drop existing tables if they exist
session.execute("DROP TABLE IF EXISTS ias_shares.data_in_db")
session.execute("DROP TABLE IF EXISTS ias_shares.db_connection_details")

# Clear existing data and create keyspace if it doesn't exist
#session.execute("DROP KEYSPACE IF EXISTS ias_shares")
#session.execute("CREATE KEYSPACE IF NOT EXISTS ias_shares WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}")
session.execute("USE ias_shares")

# Create db_connection_details table
session.execute("""
    CREATE TABLE IF NOT EXISTS db_connection_details (
        database_name TEXT,
        collections LIST<TEXT>,
        host TEXT PRIMARY KEY,
        port INT,
        username TEXT,
        password TEXT,
        get_method TEXT
    )
""")

# Create data_in_db table
session.execute("""
    CREATE TABLE IF NOT EXISTS data_in_db (
        collection_name TEXT,
        ID TEXT PRIMARY KEY,
        condition TEXT,
        gate_length TEXT,
        voltage_gate_source TEXT,
        voltage_drain_source TEXT
    )
""")

# Get connection details for databases with names starting with "ias"
db_connection_details_df = get_db_connection_details(client)

# Insert data into db_connection_details table
for _, row in db_connection_details_df.iterrows():
    session.execute("""
        INSERT INTO db_connection_details (host, database_name, collections, port, username, password, get_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (row['Connection Details']['Host'], row['Database Name'], row['Collections'],  row['Connection Details']['Port'], row['Connection Details']['username'], row['Connection Details']['password'], row['get method']))

# Fetch and display database name, collection name, ID, and timestamp of data
fetch_and_insert_data(client, session)
print("Cassandra Updated!")
# Close Cassandra connection
cluster.shutdown()
# Close the MongoDB connection
client.close()
