import pandas as pd
import json
import shutil
import boto3
from cassandra.cluster import Cluster
from pathlib import PurePath



class GetData:

    def __init__(self, my_dict):

        self.catalogue = "nfs_data"
        self.my_dict = my_dict

# get controller ip@ from  server_info.json to connect to th database
    def server_info(self):
        with open("../get_module/server_info.json", "r") as server_info:
            server_infos = json.load(server_info)
        ip = server_infos["server_ip"]
        return ip
    
# return a cassandra sesseon
    def cassandra_session(self, ip):
        return Cluster([ip], port=9042).connect("ias_shares")

## catalogue_get gets references from the DB filtred with my_dict
    def catalogue_get(self):
        # first step is to convert the dictionary to a statement to use for filtering the data in the data catalogue in my data base

        pref = list(self.my_dict.keys())
        suf = list(self.my_dict.values())

        filter = f"{pref.pop(0)} {suf.pop(0)}"
       
        while pref:
            filter = f"{pref.pop(0)} = '{suf.pop(0)}' AND {filter}"
            print(filter)
            
        statement1 = f"SELECT * FROM nfs_data  WHERE {filter} ALLOW FILTERING"
        statement2 = f"SELECT * FROM data_in_cloud WHERE {filter} ALLOW FILTERING"

        # Open the Cassandra session 
        session = self.cassandra_session(self.server_info())
        
        #execute the statement and get the data as a list of tuples
        files1 = []
        try:
            files1 = list(session.execute(statement1))
        except:
            print("Undefined column name source in table ias_shares.nfs_data")
        try:
            files2 = list(session.execute(statement2))
        except:
            print("Undefined column name source in table ias_shares.data_in_cloud")
      
        return files1+files2

    def split_url(self, url):
        _, path = url.split(":", 1)
        path = path.lstrip("/")
        bucket, key = path.split("/", 1)
        bucket_name, _ = bucket.split(".", 1)
        return [bucket_name, key]


    def nfs_get(self, src):
        target = r"data/"
        shutil.copy2(src, target)


    def s3_get(self, f_location, f_credentials, f_dest): #arg is the file location
        s3 = boto3.resource(
            service_name="s3", region_name="eu-central-1",
            aws_access_key_id=f_credentials[0],
            aws_secret_access_key=f_credentials[1]
        )
        bucket, key = self.split_url(f_location)
        p = PurePath(key)
        file_name = p.name
        file_dest = f"{f_dest}/{file_name}"
        s3.Bucket(bucket).download_file(key, file_dest)




# dict = {"f_type": "IN ('.txt')"}

# worker = GetData(dict)
# nfss = worker.catalogue_get()
# for nfs in nfss: 
#     print(nfs.f_location)
