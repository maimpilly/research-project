#This code is used for automatic update of data catalog

#!/usr/bin/env python3

from cassandra.cluster import Cluster
import json
#import netifaces as ni
import glob
from pathlib import PurePath
import os
import datetime
import boto3

#----------------------------------------------extract server information from the server_info.json file ------------------------------------------------
with open("/home/researchproject/IAS_Project/server_info.json", "r") as server_info:
    server_infos = json.load(server_info)
ip = server_infos["server_ip"]
username = server_infos["user"]
psw = server_infos["psw"]
server_name = server_infos["server_name"]

#----------------------------------------------Update the data_catalogue table with the refs of all in NFSshares files------------------------------------
mounts = []

with open('/etc/exports','r') as f:
     for line in f:
        line = line.partition('#')[0]
        line = line.rstrip()
        if line.find("IAS_") != -1: 
            mounts.append(line)


shares = [] # ---> keySpace IAS_Shares.nfss

for share in mounts:
    shares.append({"host": ip, "NFS": share.split(" ")[0], "username": username, "password": psw})

for share in mounts:
    target = share.split(" ")[0]
    dir_path = f"{target}/**/*.*"
    shared_files = glob.glob(dir_path, recursive=True)

files_list = [] #-----> keyspace: IAS_Shares.data_catalogue

for file in shared_files:
    stat = os.stat(file)
    f_modification_time = datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc)
    p = PurePath(file)
    f_name = p.name
    f_type = p.suffix
    f_location = f"/home/{username}/{file[2:]}"
    file_id = {"host": ip, "username": username, "password": psw,
               "f_name": f_name, "f_type": f_type, "f_location" : f_location,"get_methode": "ssh_file_transfer", "f_modification_time": f_modification_time.strftime("%x-%X")}
    files_list.append(file_id)
    
# here starts writing information to the database!!
## start with creating table to list all the NFSs in the active nodes

cluster = Cluster([ip])
session = cluster.connect()
session.default_timeout = 30
session.execute('''
                CREATE KEYSPACE IF NOT EXISTS IAS_Shares 
                WITH REPLICATION = { 
                'class' : 'SimpleStrategy', 'replication_factor' : 2 };
                '''
                )

session.execute('''
                CREATE TABLE IF NOT EXISTS IAS_Shares.NFSs ( host text PRIMARY KEY, 
                NFS text, username text, password text );
''')
#session.execute('TRUNCATE IAS_Shares.NFSs')
# Insert NFS info to the NFSs Table
for nfs in shares: 
    values = tuple(list(nfs.values()))
    statement = f"INSERT INTO IAS_Shares.NFSs (host, NFS, username, password) VALUES {values}"
    session.execute(statement)


## here a table for all files in the nfs_shares is created and updated with the files references.

table_name = "nfs_data"

statement = f"CREATE TABLE IF NOT EXISTS IAS_Shares.{table_name} (host text, username text, password text,f_name text, f_type text, f_location text, get_methode text, f_modification_time text, PRIMARY KEY (host, f_name));"
session.execute(statement)

## Update data Catalogue in Cassandra cluster.
#session.execute(f"TRUNCATE IAS_Shares.{table_name}")

statement = f"DELETE FROM IAS_Shares.{table_name} WHERE host = '{ip}'"
session.execute(statement)

for file in files_list:
    values = tuple(list(file.values()))
    statement = f"INSERT INTO IAS_Shares.{table_name} (host, username, password, f_name, f_type, f_location, get_methode, f_modification_time) VALUES {values}"
    session.execute(statement)

#---------------------------here a table for all files in the cloud is created and updated with the files references.--------------------------------------
# update the cloud sources liste!
if server_name == "archi_controll":

    with open("./IAS_Project/infrdep/inventory.json", "r") as inventory:
        hosts_inventory = json.load(inventory)
        
    cloud_list = hosts_inventory["all"]["children"]["cloud"]["hosts"]

    for cloud_src in cloud_list:
        aws_access_key = cloud_list[cloud_src]["aws_access_key"]
        aws_access_key_id = cloud_list[cloud_src]["aws_access_key_id"]
        region = cloud_list[cloud_src]["region"]
        src = cloud_list[cloud_src]["src"]
        get_methode = "cloud_file_transfer"

        session.execute("DROP TABLE IF EXISTS IAS_Shares.cloud_srcs")
        session.execute("DROP TABLE IF EXISTS IAS_Shares.data_in_cloud")

        statement = f"CREATE TABLE IF NOT EXISTS IAS_Shares.cloud_srcs (source text PRIMARY KEY, access_key_id text, access_key text, get_methode text, region text)"
        session.execute(statement)
        statement = f"INSERT INTO IAS_Shares.cloud_srcs (source, access_key_id, access_key, get_methode, region) VALUES ('{src}', '{aws_access_key_id}', '{aws_access_key}', '{get_methode}', '{region}')"
        session.execute(statement)

        statement = f"CREATE TABLE IF NOT EXISTS IAS_Shares.data_in_cloud (f_name text PRIMARY KEY, f_type text, f_location text, get_Methode text, source text, access_key_id text, access_key text)"
        session.execute(statement)


        S3_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_access_key,
        )


        s3 = S3_session.resource("s3")

        try:
            session.execute(f"TRUNCATE IAS_Shares.data_in_cloud")
        except:
            print("Unable to TRUNCATE IAS_Shares.data_in_cloud")

        for bucket in s3.buckets.all():
            if bucket.name.upper().find("IAS") != -1:
                for object in bucket.objects.all():
                    if object.key.find(".") != -1:
                        url = "https://"+object.bucket_name+"."+"s3."+region+src+object.key
                        p = PurePath(url)
                        f_name = p.name
                        f_type = p.suffix
                        doc = {"f_name": f_name, "f_type": f_type, "f_location": url, "get_methode": get_methode, "source": "AWS-s3-bucket", "access_key_id": aws_access_key_id, "access_key": aws_access_key}
                        values = tuple(list(doc.values()))
                        statement = f"INSERT INTO IAS_Shares.data_in_cloud (f_name, f_type, f_location, get_methode, source, access_key_id, access_key) VALUES {values}"
                        session.execute(statement)
